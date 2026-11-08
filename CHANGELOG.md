# Changelog

## 0.2.0

- First release on PyPI.
- `scrape` replaces `render`. The SDK covers scrape, tier, map, batches and monitors.
- `Megalania()` reads `MEG_API_KEY` when no key is passed.
- `wait_batch`, `read_results`, `batch_results` and `read_pages` wait for a batch, download its results (several links at once) and read pages for loaders.
- The `megalania` command: scrape, tier, map, batches, monitors and `skill install`. It talks only to https hosts, except localhost.
- `get_account`, `get_usage`, `get_domain_stats` and `rotate_webhook_secret`.
- A `schema` dict is sent as JSON text, and `read_pages` with a `schema` asks for `json`.
