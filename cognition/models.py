"""Data models for semantic search and classification."""

from pydantic import BaseModel


class Record(BaseModel):
  title: str
  comments: list[str] = []
