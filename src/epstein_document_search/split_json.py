#!/usr/bin/env python3
"""
Split the meilisearch_documents.json into multiple files under 20MB.
"""

import json
from pathlib import Path


def split_json_file(input_file, max_size_mb=18):
    """Split a large JSON array into multiple files under max_size_mb."""
    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    total_docs = len(documents)
    print(f"Total documents: {total_docs}")
    print(f"Splitting into files under {max_size_mb}MB each...")

    base_path = Path(input_file).parent
    base_name = Path(input_file).stem  # filename without extension

    current_chunk = []
    current_size = 2  # Start with 2 bytes for the [] brackets
    part_num = 1

    for doc in documents:
        # Estimate size of this document in JSON
        doc_json = json.dumps(doc, ensure_ascii=False)
        doc_size = len(doc_json.encode('utf-8')) + 3  # +3 for comma, newline, indent

        # If adding this doc would exceed limit, write current chunk
        estimated_mb = (current_size + doc_size) / (1024 * 1024)
        if current_chunk and estimated_mb > max_size_mb:
            # Write current chunk
            output_file = base_path / f"{base_name}_part{part_num}.json"
            print(f"\nWriting part {part_num}: {len(current_chunk)} documents to {output_file.name}")

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(current_chunk, f, indent=2, ensure_ascii=False)

            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"  File size: {file_size_mb:.2f} MB")

            # Start new chunk
            current_chunk = []
            current_size = 2
            part_num += 1

        # Add document to current chunk
        current_chunk.append(doc)
        current_size += doc_size

    # Write final chunk
    if current_chunk:
        output_file = base_path / f"{base_name}_part{part_num}.json"
        print(f"\nWriting part {part_num}: {len(current_chunk)} documents to {output_file.name}")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(current_chunk, f, indent=2, ensure_ascii=False)

        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"  File size: {file_size_mb:.2f} MB")


def main():
    input_file = Path(__file__).parent / "meilisearch_documents.json"

    if not input_file.exists():
        print(f"Error: {input_file} not found!")
        return

    split_json_file(input_file, max_size_mb=18)

    print("\nDone! You can now upload each part separately to Meilisearch.")


if __name__ == "__main__":
    main()
