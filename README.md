# Megalania Python SDK

**Beta.** A small client for the Megalania scraping API. One call returns a
page as HTML, Markdown or JSON. You get the body, the response headers as
typed fields, and a `MegalaniaError` with the error code and message.

- It retries once on a 429, after `Retry-After`, and never on anything else.
- Every call sends an `Idempotency-Key`, so a repeat is never charged twice.
- The types are generated from the Megalania OpenAPI document.

## Install

Python 3.10 or newer.

```sh
pip install git+https://github.com/megalania/megalania-python
```

## One page

```python
import os

from megalania import Megalania, MegalaniaError

with Megalania(os.environ["MEG_API_KEY"]) as meg:
    try:
        page = meg.render("https://example.com/", response_types="markdown")
    except MegalaniaError as e:
        print(e.status, e.code, e.message, e.request_id)
        raise
    print(page.headers.credits_charged, page.text[:200])
```

The client calls `https://get.megalania.io` unless you pass `base_url`.

## Docs

The full guide is at https://docs.megalania.io/guides/sdk-python.

## License

MIT. See `LICENSE`. Security reports: see `SECURITY.md`.
