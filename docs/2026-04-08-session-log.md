# Session Log: 2026-04-08

## Summary
Built a complete RAG (Retrieval-Augmented Generation) system for searching 2,425 academic articles from The Hedgehog Review and The New Atlantis.

---

## What Was Built

### 1. Article Summarization Pipeline
- **Script:** `summarize_article.py` — Summarizes a single article using OpenAI API
- **Script:** `run_all_summaries_parallel.py` — Batch summarizes all articles (10 parallel workers)
- **Model:** `gpt-5.4-nano` (cheapest, performed as well as larger models)
- **Output:** `summaries/` folder with 2,425 JSON files containing metadata + ~200 word summaries
- **Cost:** ~$2.60 for all summaries

### 2. OpenAI Vector Store (RAG Database)
- **Store ID:** `vs_69d6bf7a8124819188667e813b7dc913`
- **Contents:** All 2,425 summary JSON files uploaded
- **Cost:** ~$0.001/day storage, ~$0.0025/query

### 3. GitHub Repository
- **Repo:** https://github.com/sam-hendel/RAG-article-search-and-read
- **Contents:**
  - `README.md` — Setup and usage instructions
  - `search.py` — Search RAG and download top 5 articles
  - `search_and_push.py` — Search + auto git push
  - `config.json` — Vector store settings
  - `searches/` — Example search results with articles + SUMMARY.md

### 4. Example Searches Completed
- `searches/war-and-memory/` — 5 articles
- `searches/professional-sports/` — 5 articles
- `searches/thorstein-veblen/` — 13 articles (text search, not RAG)

---

## Key Files & Locations

```
C:\Users\sjhen\Documents\33_article-scraping\
├── articles/
│   ├── hedgehog-review/     # 1,219 .md articles
│   └── new-atlantis/        # 1,206 .md articles
├── summaries/               # 2,425 .json summary files
├── summarize_article.py     # Single article summarizer
├── run_all_summaries_parallel.py  # Batch summarizer
├── find_veblen.py           # Text search example
├── vector_store_id.txt      # Contains: vs_69d6bf7a8124819188667e813b7dc913
└── docs/logs/               # Session logs

C:\Users\sjhen\Documents\RAG-article-search-and-read\
├── README.md
├── search.py
├── search_and_push.py
├── config.json
└── searches/
    ├── war-and-memory/
    ├── professional-sports/
    └── thorstein-veblen/
```

---

## How to Resume

### To search for articles:
```bash
cd C:\Users\sjhen\Documents\RAG-article-search-and-read
python search.py "your query"
# or
python search_and_push.py "your query"  # auto-pushes to GitHub
```

### To find articles by text (not semantic):
```bash
cd C:\Users\sjhen\Documents\33_article-scraping
# Edit find_veblen.py to change SEARCH_STRING, then run
python find_veblen.py
```

### Vector Store Details
- **ID:** `vs_69d6bf7a8124819188667e813b7dc913`
- **API:** `client.vector_stores.search(vector_store_id=ID, query="...", max_num_results=5)`
- **Max results per query:** 50

---

## Costs Summary
| Item | Cost |
|------|------|
| Summarization (2,425 articles, nano) | ~$2.60 |
| Vector store storage | ~$0.03/month |
| Per search query | ~$0.0025 |

---

## Potential Next Steps
- [ ] Add more publications to the corpus
- [ ] Build a web interface for searching
- [ ] Add filtering by publication, date, or section
- [ ] Create embeddings locally (FAISS) for free unlimited queries
- [ ] Add "answer with context" feature using GPT to synthesize results

---

## Session Notes
- gpt-5.4-nano performed as well as gpt-5.4 and gpt-5.4-mini for summarization (experiment in `experiment_v01/`)
- Parallel processing (10 workers) reduced summarization time from ~70 min to ~7 min
- Vector store upload took ~30 min with 10 parallel workers
- Text search for "Thorstein Veblen" found 13 articles
