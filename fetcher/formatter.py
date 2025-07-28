from .models import Record


class OutputFormatter:
    """Formatter for console output of links and comments."""

    @staticmethod
    def format_record(record: Record) -> str:
        """Format a single record for console output."""
        output = []
        output.append("=" * 80)
        output.append(f"Record ID: {record.id}")
        output.append(f"Type: {record.type}")
        output.append(f"Title: {record.title}")
        output.append(f"Description: {record.description}")
        output.append("")

        if record.comments:
            output.append(f"Comments ({len(record.comments)}):")
            output.append("-" * 40)
            for i, comment in enumerate(record.comments, 1):
                output.append(f"  [{i}] {comment}")
            output.append("")
        else:
            output.append("No comments available.")
            output.append("")

        return "\n".join(output)
