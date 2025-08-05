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

        # Process in batches to show progress and manage memory
        all_embeddings = []

        batches = [
            inputs[i : i + batch_size] for i in range(0, len(inputs), batch_size)
        ]
        progress_bar = tqdm(batches, desc="Encoding batches", unit="batch")

        for batch in progress_bar:
            # Tokenize the batch
            encoded_inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)

            with torch.no_grad():
                model_output = self.model(**encoded_inputs)

            # Mean pooling
            attention_mask = encoded_inputs["attention_mask"]
            token_embeddings = model_output.last_hidden_state

            input_mask_expanded = (
                attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            )
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            embeddings = sum_embeddings / sum_mask

            if normalize:
                embeddings = F.normalize(embeddings, p=2, dim=1)

            all_embeddings.append(embeddings)

            # Update progress description
            progress_bar.set_postfix(
                {
                    "processed": f"{min((progress_bar.n + 1) * batch_size, len(inputs))}/{len(inputs)}"
                }
            )

        # Concatenate all batch embeddings
        return torch.cat(all_embeddings, dim=0)
