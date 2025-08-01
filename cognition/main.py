import os
import sys

from cognition.formatter import Formatter
from cognition.parser import Parser

from .config import Config


def main():
    config = Config()
    parser = Parser()
    formatter = Formatter()

    try:
        print(f"Using model: {config.model_name}")

        # tokenizer = build_tokenizer(config)
        # model = build_model(config)

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sample_file_path = os.path.join(project_root, "tmp", "20250731_212553_microblog.json")
        data = parser.parse(sample_file_path)

        inputs = [formatter.format_record(item) for item in data]

        print(f"Parsed data")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
