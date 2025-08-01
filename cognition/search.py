"""Semantic search functionality."""

import torch
from transformers import AutoModel, AutoTokenizer

from cognition.config import Config


def build_model(config: Config) -> AutoModel:
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    model = AutoModel.from_pretrained(config.model_name).to(device)
    return model


def build_tokenizer(config: Config) -> AutoTokenizer:
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    return tokenizer
