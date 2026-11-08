# llama-index-readers-megalania

LlamaIndex reader for the [Megalania](https://megalania.io) scraping API.

```sh
pip install llama-index-readers-megalania
export MEG_API_KEY=...
```

```python
from llama_index.readers.megalania import MegalaniaReader

docs = MegalaniaReader().load_data(["https://docs.megalania.io/"])
crawl = MegalaniaReader().load_data("https://docs.megalania.io/", crawl={"max_pages": 20})
```

The documents hold Markdown with `source`, `request_id`, `credits_charged` and `target_status` in the metadata.
A blocked page raises `MegalaniaError`; set `continue_on_failure=True` to skip it. Blocked pages and errors are free.
For agents, connect the Megalania MCP server with `llama-index-tools-mcp`.

Guide: https://docs.megalania.io/integrations/llamaindex. MIT license.
