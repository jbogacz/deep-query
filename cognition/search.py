"""Semantic search functionality."""

import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

from cognition.config import Config
from cognition.utils import local_device


class EmbeddingEncoder:
    def __init__(self, config: Config, device=None):
        if device is None:
            self.device = local_device()
        else:
            self.device = device

        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModel.from_pretrained(config.model_name).to(self.device)

        self.model.eval()

    def encode(self, inputs, normalize=True, batch_size=32):
        """Encode the inputs into embeddings with optional progress tracking."""

        if isinstance(inputs, str):
            inputs = [inputs]

        all_embeddings = []

        # Split input texts into manageable chunks for batch processing
        # This prevents GPU memory overflow and enables progress tracking
        # Example: 1000 texts with batch_size=32 → 32 batches (31 full + 1 partial)
        batches = [
            inputs[i : i + batch_size] for i in range(0, len(inputs), batch_size)
        ]

        # Create progress bar to track batch processing
        # Shows which batch we're on and estimated completion time
        progress_bar = tqdm(batches, desc="Encoding batches", unit="batch")

        for batch in progress_bar:
            # STEP 1: TOKENIZATION
            # Convert text strings to numerical token IDs that the model understands
            # - padding=True: Make all sequences same length (pad shorter ones)
            # - truncation=True: Cut sequences longer than max_length
            # - max_length=512: BERT-style models typically use this limit
            # - return_tensors="pt": Return PyTorch tensors instead of lists
            encoded_inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)  # Move tensors to GPU/MPS for processing

            # STEP 2: MODEL INFERENCE
            # Pass tokenized inputs through the transformer model
            # torch.no_grad() disables gradient computation for efficiency (we're not training)
            with torch.no_grad():
                model_output = self.model(**encoded_inputs)

            # STEP 3: EXTRACT TOKEN-LEVEL EMBEDDINGS
            # Get the attention mask (1s for real tokens, 0s for padding)
            # This tells us which positions contain actual content vs padding
            attention_mask = encoded_inputs["attention_mask"]

            # Extract hidden states from the last transformer layer
            # Shape: [batch_size, sequence_length, hidden_size]
            # Each token position gets its own embedding vector
            token_embeddings = model_output.last_hidden_state

            # STEP 4: MEAN POOLING PREPARATION
            # Expand attention mask to match embedding dimensions
            # Original mask shape: [batch_size, sequence_length]
            # After expansion: [batch_size, sequence_length, hidden_size]
            # This allows element-wise multiplication with token embeddings
            input_mask_expanded = (
                attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            )

            # STEP 5: WEIGHTED SUMMATION
            # Multiply each token embedding by its mask value
            # Real tokens: embedding * 1 = embedding (kept)
            # Padding tokens: embedding * 0 = zero (ignored)
            # Then sum along sequence dimension to get sentence-level embedding
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)

            # Count how many real (non-padding) tokens each sequence has
            # This is the denominator for computing the average
            # clamp(min=1e-9) prevents division by zero if sequence is all padding
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)

            # STEP 6: COMPUTE MEAN POOLING
            # Divide sum by count to get average embedding across real tokens
            # This gives us one fixed-size vector per input text
            embeddings = sum_embeddings / sum_mask

            # STEP 7: OPTIONAL NORMALIZATION
            # Convert to unit vectors (length = 1) if requested
            # This makes cosine similarity equivalent to dot product
            # and ensures all embeddings have same magnitude
            if normalize:
                embeddings = F.normalize(embeddings, p=2, dim=1)

            # STEP 8: COLLECT BATCH RESULTS
            # Store this batch's embeddings for later concatenation
            # Each batch produces tensor of shape [batch_size, hidden_size]
            all_embeddings.append(embeddings)

            # STEP 9: UPDATE PROGRESS DISPLAY
            # Show how many texts have been processed so far
            # Helps user track progress and estimate remaining time
            progress_bar.set_postfix(
                {
                    "processed": f"{min((progress_bar.n + 1) * batch_size, len(inputs))}/{len(inputs)}"
                }
            )

        # STEP 10: COMBINE ALL BATCHES
        # Concatenate embeddings from all batches into single tensor
        # Final shape: [total_inputs, hidden_size]
        # Now we have one embedding vector per input text
        return torch.cat(all_embeddings, dim=0)
