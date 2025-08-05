"""Data models for semantic search and classification."""

import torch
from transformers import AutoModel, AutoModelForMaskedLM, AutoTokenizer
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from cognition.config import Config


def build_tokenizer(config: Config) -> PreTrainedTokenizerBase:
    """Build and return a tokenizer from the configuration."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        return tokenizer
    except Exception as e:
        print(f"Error loading tokenizer for {config.model_name}: {e}")
        raise


def build_model(config: Config) -> PreTrainedModel:
    """Build and return a model from the configuration."""
    try:
        model = AutoModelForMaskedLM.from_pretrained(config.model_name)
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
        return model.to(device).eval()
    except Exception as e:
        print(f"Error loading model for {config.model_name}: {e}")
        raise
