import os
import sys

import torch.nn.functional as F

from cognition.formatter import Formatter
from cognition.parser import Parser
from cognition.search import EmbeddingEncoder

from .config import Config


def main():
    config = Config()
    parser = Parser()
    formatter = Formatter()
    encoder = EmbeddingEncoder(config)

    try:
        print(f"Using model: {config.model_name}")

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sample_file_path = os.path.join(
            project_root, "tmp", "20250731_212553_microblog.json"
        )
        texts = parser.parse(sample_file_path)
        inputs = [formatter.format_record(item) for item in texts]

        inputs_embedding = encoder.encode(inputs)
        query_embedding = encoder.encode("Biznes")

        similarities = F.cosine_similarity(query_embedding, inputs_embedding)

        results = sorted(
            zip(inputs, similarities), key=lambda x: float(x[1]), reverse=True
        )

        # Display results
        print("\nTop 10 search results:")
        for i, (doc, score) in enumerate(results[:10], 1):
            print(f"\n{'-' * 40}")
            print(f"Result #{i} | Score: {score:.4f}")
            print(f"{'-' * 40}")
            print(f"{doc}")

        print("\nDONE")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
