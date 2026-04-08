#!/usr/bin/env python3
"""Search RAG database and download top articles."""

import sys
import json
import shutil
from pathlib import Path
from openai import OpenAI

VECTOR_STORE_ID = "vs_69d6bf7a8124819188667e813b7dc913"
ARTICLES_DIR = Path(__file__).parent.parent / "33_article-scraping" / "articles"
SUMMARIES_DIR = Path(__file__).parent.parent / "33_article-scraping" / "summaries"
SEARCHES_DIR = Path(__file__).parent / "searches"

client = OpenAI()


def search_articles(query, max_results=5):
    """Search the vector store and return results."""
    results = client.vector_stores.search(
        vector_store_id=VECTOR_STORE_ID,
        query=query,
        max_num_results=max_results,
    )
    return results.data


def get_summary(filename):
    """Load summary from JSON file."""
    json_path = SUMMARIES_DIR / filename
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def find_article_md(filename):
    """Find the original .md file for an article."""
    stem = Path(filename).stem

    # Search in both publication folders
    for pub in ["hedgehog-review", "new-atlantis"]:
        md_path = ARTICLES_DIR / pub / f"{stem}.md"
        if md_path.exists():
            return md_path
    return None


def create_summary_md(results, summaries):
    """Generate SUMMARY.md content."""
    lines = ["# Search Results\n"]

    for i, (result, summary) in enumerate(zip(results, summaries), 1):
        if summary:
            lines.append(f"## {i}. {summary.get('title', 'Untitled')}\n")
            lines.append(f"**Publication:** {summary.get('publication', 'Unknown')}")
            lines.append(f"**Date:** {summary.get('date', 'Unknown')}")
            if summary.get('issue'):
                lines.append(f"**Issue:** {summary.get('issue')}")
            if summary.get('section'):
                lines.append(f"**Section:** {summary.get('section')}")
            lines.append(f"**Word Count:** {summary.get('word_count', 'Unknown')}")
            lines.append(f"**Relevance Score:** {result.score:.3f}")
            lines.append("")
            lines.append(f"### Summary\n")
            lines.append(summary.get('summary', 'No summary available.'))
            lines.append("")
            lines.append("---\n")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        print('Example: python search.py "war and memory"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    folder_name = query.lower().replace(" ", "-")

    print(f"Searching: {query}")
    print("=" * 50)

    # Search
    results = search_articles(query)

    if not results:
        print("No results found.")
        sys.exit(1)

    # Create output folder
    output_dir = SEARCHES_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each result
    summaries = []
    for i, result in enumerate(results, 1):
        filename = result.filename
        score = result.score

        print(f"[{i}] {score:.3f} - {filename}")

        # Get summary
        summary = get_summary(filename)
        summaries.append(summary)

        # Copy .md file
        md_path = find_article_md(filename)
        if md_path:
            dest = output_dir / md_path.name
            shutil.copy(md_path, dest)
            print(f"    -> Copied {md_path.name}")
        else:
            print(f"    -> WARNING: .md file not found")

    # Generate SUMMARY.md
    summary_content = create_summary_md(results, summaries)
    summary_path = output_dir / "SUMMARY.md"
    summary_path.write_text(summary_content, encoding='utf-8')
    print(f"\nGenerated: {summary_path}")

    print(f"\nDone! Results in: {output_dir}")


if __name__ == "__main__":
    main()
