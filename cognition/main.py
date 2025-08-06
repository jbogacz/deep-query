import os
import sys

import torch.nn.functional as F

from cognition.formatter import Formatter
from cognition.parser import Parser
from cognition.search import EmbeddingEncoder

from .config import Config


def main():
    # Initialize configuration and components
    # Config: Holds model settings (model name, device preferences, etc.)
    # Parser: Converts JSON data into structured Record objects
    # Formatter: Transforms records into text suitable for embedding
    # Encoder: Generates semantic embeddings from text using transformer models
    config = Config()
    parser = Parser()
    formatter = Formatter()
    encoder = EmbeddingEncoder(config)

    try:
        print(f"Using model: {config.model_name}")

        # STEP 1: LOAD AND PARSE DATA
        # Construct path to the microblog JSON file containing forum posts
        # This file contains structured data with posts, comments, metadata
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sample_file_path = os.path.join(
            project_root, "tmp", "20250731_212553_microblog.json"
        )

        # Parse JSON file into Record objects with structured fields
        # Each record contains: id, title, description, source, type, created_at, comments
        texts = parser.parse(sample_file_path)

        # STEP 2: FORMAT FOR EMBEDDING
        # Convert structured records into natural language text
        # This combines title, description, and comments into coherent passages
        # Example: "Title: [post title]\nContent: [description]\nComments: [comment1, comment2...]"
        inputs = [formatter.format_record(item) for item in texts]

        # STEP 3: GENERATE DOCUMENT EMBEDDINGS
        # Transform each formatted text into a dense vector representation
        # Uses transformer model (e.g., BERT) to capture semantic meaning
        # Output shape: [num_documents, embedding_dimension] (e.g., [1000, 768])
        # Each row is a high-dimensional vector representing one document's meaning
        inputs_embedding = encoder.encode(inputs)

        # STEP 4: GENERATE QUERY EMBEDDING
        # Convert search query into same embedding space as documents
        # Must use identical model and processing to ensure compatibility
        # Output shape: [1, embedding_dimension] (e.g., [1, 768])
        query_embedding = encoder.encode("Biznes")

        # STEP 5: COMPUTE SEMANTIC SIMILARITY
        # Calculate cosine similarity between query and all documents
        #
        # WHY COSINE SIMILARITY?
        # =====================
        # 1. SEMANTIC RELEVANCE: Measures angle between vectors, not magnitude
        #    - Documents of different lengths get fair comparison
        #    - Focuses on semantic direction rather than vector size
        #
        # 2. NORMALIZED COMPARISON: Range is always [-1, 1]
        #    - 1.0 = identical semantic meaning (parallel vectors)
        #    - 0.0 = no semantic relationship (orthogonal vectors)
        #    - -1.0 = opposite meaning (antiparallel vectors)
        #
        # 3. LENGTH INVARIANCE: Short and long documents compared fairly
        #    - "Business" vs "Business is important for economy"
        #    - Both could have similar cosine similarity to query "Biznes"
        #    - Euclidean distance would unfairly penalize longer text
        #
        # 4. EFFICIENT COMPUTATION: Simple dot product after normalization
        #    - Our embeddings are already normalized (unit vectors)
        #    - cosine(A,B) = A·B when ||A|| = ||B|| = 1
        #
        # 5. PROVEN EFFECTIVENESS: Standard in information retrieval
        #    - Works well with transformer embeddings
        #    - Handles high-dimensional sparse spaces effectively
        similarities = F.cosine_similarity(query_embedding, inputs_embedding)

        # STEP 6: RANK RESULTS BY RELEVANCE
        # Sort documents by similarity score in descending order
        # Higher scores = more semantically similar to query
        # zip() pairs each document with its similarity score
        # key=lambda extracts score for sorting, reverse=True for descending order
        results = sorted(
            zip(inputs, similarities), key=lambda x: float(x[1]), reverse=True
        )

        # STEP 7: DISPLAY TOP RESULTS
        # Show the 10 most relevant documents with their similarity scores
        # Provides visual feedback on search quality and ranking confidence
        print("\nTop 10 search results:")
        for i, (doc, score) in enumerate(results[:10], 1):
            print(f"\n{'-' * 40}")
            print(f"Result #{i} | Score: {score:.4f}")  # 4 decimal precision
            print(f"{'-' * 40}")
            print(f"{doc}")

        print("\nDONE")

    except Exception as e:
        # STEP 8: ERROR HANDLING
        # Catch and display any errors during processing
        # Common issues: file not found, CUDA memory errors, model loading failures
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
