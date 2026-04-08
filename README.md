# RAG Article Search and Read

Search a curated database of 2,400+ article summaries from The Hedgehog Review and The New Atlantis using semantic search.

## Setup

1. Install dependencies:
```bash
pip install openai
```

2. Set your OpenAI API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-key-here"

# macOS/Linux
export OPENAI_API_KEY="your-key-here"
```

## Usage

Search for articles and download the top 5 matches:

```bash
python search.py "your search query here"
```

### Example

```bash
python search.py "war and memory"
```

This will:
1. Search the RAG database for semantically similar articles
2. Create a folder `searches/war-and-memory/`
3. Copy the top 5 matching article `.md` files into that folder
4. Generate a `SUMMARY.md` with previews of each article

## Output Structure

```
searches/
  war-and-memory/
    SUMMARY.md                           # Summaries of all 5 articles
    interview-with-james-e-young.md      # Full article text
    jay-winters-remembering-war.md
    ...
```

## Vector Store

- **Store ID:** `vs_69d6bf7a8124819188667e813b7dc913`
- **Articles:** 2,424 summaries from Hedgehog Review and New Atlantis
- **Search:** OpenAI Vector Store semantic search

## Cost

- ~$0.0025 per search query
- Storage: ~$0.001/day
