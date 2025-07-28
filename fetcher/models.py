from enum import Enum
from typing import List

from pydantic import BaseModel


class RecordType(str, Enum):
    ARTICLE = "article/link"
    ENTRY = "entry/microblog"


class Record(BaseModel):
    id: str
    title: str
    description: str
    type: RecordType
    comments: List[str] = []

    def __str__(self):
        """String representation of the record."""
        return f"Record(id={self.id}, type={self.type}, title={self.title}, description={self.description}, comments_count={len(self.comments)})"

    def add_comment(self, comment: str):
        """Add a comment to the record."""
        self.comments.append(comment)

    def set_comments(self, comments: List[str]):
        """Set comments for the record."""
        self.comments = comments
