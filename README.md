# Megalania Python SDK

**Beta.** A small client for the Megalania scraping API. One call returns a
page as HTML, Markdown or JSON, and batches, monitors, map and tier have a
method each. You get the body, the response headers as
typed fields, and a `MegalaniaError` with the error code and message.

- It retries once on a 429, after `Retry-After`, and never on anything else.
- Every scrape, map and create call sends an `Idempotency-Key`, so a repeat is never charged twice.
- The types are generated from the Megalania OpenAPI document.

## Install

Python 3.10 or newer.

```sh
pip install megalania
```

## One page

```python
import os

from megalania import Megalania, MegalaniaError

with Megalania(os.environ["MEG_API_KEY"]) as meg:
    try:
        page = meg.scrape("https://example.com/", response_types="markdown")
    except MegalaniaError as e:
        print(e.status, e.code, e.message, e.request_id)
        raise
    print(page.headers.credits_charged, page.text[:200])
```

The client calls `https://get.megalania.io` unless you pass `base_url`.

Batches, monitors, map and tier have their own methods, named after their
REST operation: `get_tier`, `map_site`, `create_batch`, `get_batch`,
`list_batch_items`, `cancel_batch`, `create_monitor`, `list_monitors` and
more. They call `https://api.megalania.io` unless you pass `api_url`:

```python
with Megalania(os.environ["MEG_API_KEY"]) as meg:
    batch = meg.create_batch(["https://docs.megalania.io/start/quickstart"], response_types="markdown")
    print(meg.get_batch(batch["id"]))
```

## Docs

The full guide is at https://docs.megalania.io/guides/sdk-python.

## License

MIT. See `LICENSE`. Security reports: see `SECURITY.md`.
