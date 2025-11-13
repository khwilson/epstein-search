# Epstein Document Search

A searchable database of Epstein court documents using Meilisearch for fast, full-text search capabilities. Forked from https://github.com/paulgp/epstein-document-search

## Overview

This project processes court documents related to the Epstein case, extracts metadata (case numbers, page numbers, etc.), and indexes them in Meilisearch for easy searching. It includes a clean web interface for querying the documents.

## Features

- **Full-text search** across all documents
- **Page-level indexing** for precise results
- **Metadata extraction** including case numbers, document IDs, and page numbers
- **Filter by folder** to narrow searches
- **Highlighted search results** showing matching terms
- **Expandable results** to read full document pages

## Project Structure

```
.
├── website/
│   └── index.html              # Web-based search interface
│   └── documents.json          # Processed documents for serving (big, but not quite too big for GitHub)
├── prepare_for_meilisearch.py  # Process documents for indexing
├── split_json.py               # Split large JSON files for upload
├── data/
│   └── house_dems.pdf          # Sample document
│   └── house_dems.txt          # Extracted text from sample document
```

Note: The actual document folders (001/, 002/) and generated JSON files are excluded from git due to their size.

## Document Sources

- **Main document folders**: [Google Drive](https://drive.google.com/drive/folders/1TrGxDGQLDLZu1vvvZDBAh-e7wN3y6Hoz) - Contains folders 001/ and 002/ with court documents
- **House Democrats packet**: [Original PDF](https://oversightdemocrats.house.gov/sites/evo-subsites/democrats-oversight.house.gov/files/evo-media-document/packet_redacted_noid.pdf) - Converted to text as `house_dems.txt`

## Requirements

- uv
- Modern web browser

## Setup

### 1. Obtain Documents

Download documents from the [Google Drive folder](https://drive.google.com/drive/folders/1TrGxDGQLDLZu1vvvZDBAh-e7wN3y6Hoz) and place the extracted court document `.txt` files in numbered folders (e.g., `001/`, `002/`) and place them in the `/data` folder.

### 2. Process Documents

Run the preparation script to convert documents into Meilisearch-ready JSON:

```bash
uv run python3 -m epstein_document_search.prepare PATH/TO/DOCUMENTS website/documents.json
```

This will:
- Scan all `.txt` files in the directory
- Split documents by page
- Extract metadata (case numbers, page numbers)
- Generate `documents.json`

### 3. Run Locally

If you want to run locally, use

```bash
cd website
uv run python3 -m http.server
```

### 4. Push to GitHub Pages

There is an included GitHub action that will push to a github pages instance. See `.github/workflows/deploy.yml`.

## Document Format

The processing script expects documents with this format:

```
Case 1:19-cv-03377 Document 1-3 Filed 04/16/19 Page 1 of 3
[Document content here...]
```

Each document is split into pages and indexed with:
- `id`: Unique identifier for each page
- `content`: Full text content of the page
- `document_id`: Filename without extension
- `folder`: Source folder (001, 002, etc.)
- `page_number`: Current page number
- `total_pages`: Total pages in document
- `case_number`: Extracted case number
- `source_file`: Relative path to original file

## Usage Tips

- **Exact phrases**: Use quotes for exact phrase matching: `"Jeffrey Epstein"`
- **Folder filtering**: Select a specific folder to narrow results
- **Case numbers**: Search by case number to find all related documents
- **Load more**: Use the "Load More" button to fetch additional results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is for educational and research purposes. The court documents themselves are public records.

## Acknowledgments

- Built with [Meilisearch](https://www.meilisearch.com) for fast, typo-tolerant search
- Court documents are public records from various legal proceedings
