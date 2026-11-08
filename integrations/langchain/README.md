# langchain-megalania

LangChain document loader and tools for the [Megalania](https://megalania.io) scraping API.

```sh
pip install langchain-megalania
export MEG_API_KEY=...
```

```python
from langchain_megalania import MegalaniaLoader, megalania_tools

docs = MegalaniaLoader(["https://docs.megalania.io/"]).load()
crawl = MegalaniaLoader("https://docs.megalania.io/", crawl={"max_pages": 20}).load()
tools = megalania_tools()
```

- The loader returns Markdown with `source`, `request_id`, `credits_charged` and `target_status` in the metadata.
  A blocked page raises `MegalaniaError`; pass `continue_on_failure=True` to skip it.
- The tools are `scrape`, `map_site`, `create_batch` and `get_batch`. Each page costs at most
  `max_credits` (default 128); pass `megalania_tools(max_credits=...)` to raise it.
- One `create_batch` call takes at most `max_pages` pages (default 100), crawls included;
  pass `megalania_tools(max_pages=...)` to raise it. The agent can raise neither cap.
- Blocked pages and errors are free.

Guide: https://docs.megalania.io/integrations/langchain. MIT license.
