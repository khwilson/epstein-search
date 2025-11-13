#!/usr/bin/env python3
"""
Prepare Epstein document txt files for Meilisearch indexing.
Splits documents by page and extracts metadata.
"""

import os
import re
import json
from pathlib import Path


def extract_case_number(text):
    """Extract case number from document text (e.g., 'Case 1:19-cv-03377')."""
    match = re.search(r'Case\s+[\d:]+[-\w]+', text)
    return match.group(0) if match else None


def extract_page_info(text):
    """Extract page number information (e.g., 'Page 1 of 3')."""
    match = re.search(r'Page\s+(\d+)\s+of\s+(\d+)', text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def split_into_pages(content):
    """
    Split document content into pages based on page markers.
    Returns list of (page_content, page_num, total_pages) tuples.
    """
    # Split on case document markers that include "Page X of Y"
    # Pattern: "Case 1:19-cv-03377 Document 1-3 Filed 04/16/19 Page 2 of 3"
    page_pattern = r'Case\s+[\d:]+[-\w]+\s+Document\s+[\d-]+\s+Filed\s+[\d/]+\s+Page\s+\d+\s+of\s+\d+'

    # Find all page markers and their positions
    pages = []
    markers = list(re.finditer(page_pattern, content))

    if not markers:
        # No page markers found, treat entire document as one page
        page_num, total_pages = extract_page_info(content)
        return [(content, page_num, total_pages)]

    # Process each page
    for i, marker in enumerate(markers):
        # Get the content from this marker to the next (or end of file)
        start_pos = marker.start()
        end_pos = markers[i + 1].start() if i + 1 < len(markers) else len(content)

        page_content = content[start_pos:end_pos].strip()
        page_num, total_pages = extract_page_info(page_content)

        pages.append((page_content, page_num, total_pages))

    return pages


def process_file(filepath, base_path):
    """
    Process a single txt file and return list of document chunks.

    Args:
        filepath: Path to the txt file
        base_path: Base directory path for calculating relative paths

    Returns:
        List of document dictionaries ready for Meilisearch
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

    # Extract metadata
    relative_path = Path(filepath).relative_to(base_path)
    folder = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
    document_id = Path(filepath).stem  # filename without extension

    # Extract case number from content (usually in first few lines)
    case_number = extract_case_number(content[:500])

    # Split into pages
    pages = split_into_pages(content)

    # Create document chunks
    documents = []
    for idx, (page_content, page_num, total_pages) in enumerate(pages):
        # Generate unique ID for each chunk
        chunk_id = f"{document_id}_page_{page_num if page_num else idx + 1}"

        doc = {
            "id": chunk_id,
            "content": page_content,
            "document_id": document_id,
            "folder": folder,
            "page_number": page_num if page_num else idx + 1,
            "total_pages": total_pages,
            "case_number": case_number,
            "source_file": str(relative_path)
        }
        documents.append(doc)

    return documents


def main():
    """Main function to process all txt files and generate JSON output."""
    base_path = Path(__file__).parent
    output_file = base_path / "meilisearch_documents.json"

    print(f"Scanning directory: {base_path}")
    print("Finding all .txt files...")

    # Find all txt files
    txt_files = list(base_path.glob("**/*.txt"))
    print(f"Found {len(txt_files)} txt files")

    # Process all files
    all_documents = []
    for idx, filepath in enumerate(txt_files, 1):
        if idx % 10 == 0:
            print(f"Processing file {idx}/{len(txt_files)}...")

        documents = process_file(filepath, base_path)
        all_documents.extend(documents)

    print(f"\nTotal chunks created: {len(all_documents)}")
    print(f"Writing to: {output_file}")

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_documents, f, indent=2, ensure_ascii=False)

    print("Done!")
    print(f"\nNext steps:")
    print(f"1. Upload to Meilisearch using their API or SDK")
    print(f"2. Configure searchable attributes: content, document_id, case_number")
    print(f"3. Configure filterable attributes: folder, page_number, case_number")


if __name__ == "__main__":
    main()
