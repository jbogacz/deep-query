import re


class Formatter:
    def format_record(self, record: dict) -> str:
        result = ""
        result += f"Title: ${record.get('title', 'No Title')}\n"
        result += "\n"
        result += "Comments:\n"

        comments = [
            clean
            for comment in record.get("comments", [])
            if (clean := self._clean_comment(comment))
        ]
        result += "\n".join([f"- {comment}" for comment in comments if comment])
        return result

    def _clean_comment(self, comment: str) -> str | None:
        """Clean and format a single comment."""
        comment = comment.strip()
        comment = re.sub(r"@[^ ]+\s*", "", comment)  # Remove mentions
        comment = re.sub("\n", "", comment)  # Remove mentions
        comment = comment[1:] if comment and not comment[0].isalnum() else comment
        return comment if comment else None
