"""Data models for forum entities."""

from typing import List

from pydantic import BaseModel


class Comment(BaseModel):
    """Model for a comment/conversation entry."""

    id: str
    author: str
    content: str


class Link(BaseModel):
    """Model for a forum link/article."""

    id: str
    title: str
    description: str


class Record(BaseModel):
    """Model for a record containing a link and its comments."""

    id: str
    title: str
    description: str
    comments: List[str] = []

    def __str__(self):
        """String representation of the record."""
        return f"Record(id={self.id}, title={self.title}, description={self.description}, comments_count={len(self.comments)})"

    def add_comment(self, comment: str):
        """Add a comment to the record."""
        self.comments.append(comment)

    def set_comments(self, comments: List[str]):
        """Set comments for the record."""
        self.comments = comments
