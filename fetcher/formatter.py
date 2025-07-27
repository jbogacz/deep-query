"""Output formatter for displaying links and comments."""

from typing import List
from .models import Link, Comment


class OutputFormatter:
    """Formatter for console output of links and comments."""

    @staticmethod
    def format_link(link: Link) -> str:
        """Format a single link with its comments for console output."""
        output = []
        output.append("=" * 80)
        output.append(f"Link ID: {link.id}")
        output.append(f"Title: {link.title}")
        output.append(f"Author: {link.author}")
        output.append(f"Created: {link.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"URL: {link.url}")
        output.append("")
        output.append("Content:")
        output.append("-" * 40)
        output.append(link.description)
        output.append("")

        if link.comments:
            output.append(f"Comments ({len(link.comments)}):")
            output.append("-" * 40)

            for i, comment in enumerate(link.comments, 1):
                output.append(
                    f"  [{i}] {comment.author} ({comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}):"
                )
                # Indent comment content
                comment_lines = comment.content.split("\n")
                for line in comment_lines:
                    output.append(f"      {line}")
                output.append("")
        else:
            output.append("No comments available.")
            output.append("")

        return "\n".join(output)

    @staticmethod
    def format_links(links: List[Link]) -> str:
        """Format multiple links for console output."""
        if not links:
            return "No links found."

        output = []
        output.append(f"\nFetched {len(links)} links:\n")

        for link in links:
            output.append(OutputFormatter.format_link(link))

        return "\n".join(output)
