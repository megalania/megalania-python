# Changelog

## 0.1.0

- `MegalaniaLoader`: pages or a crawl as LangChain documents.
- `megalania_tools()`: scrape, map_site, create_batch and get_batch as LangChain tools, capped at 128 credits a page and 100 pages a batch by default.
- `megalania_tools()` has an `extract` tool: fields by CSS rules or by a JSON Schema.
