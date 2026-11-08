import dataclasses
import json
import logging
import os
import time
import typing
import urllib.parse
import uuid
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import httpx


@dataclasses.dataclass(frozen=True)
class Headers:
    request_id: str | None = None
    cache_control: str | None = None
    content_security_policy: str | None = None
    content_type_options: str | None = None
    referrer_policy: str | None = None
    credits_charged: int | None = None
    credits_route: int | None = None
    credits_output: int | None = None
    credits_other: int | None = None
    engine: str | None = None
    target_status: int | None = None
    timing_target_ms: int | None = None
    route: str | None = None
    geo: str | None = None
    identity: str | None = None
    billing: str | None = None
    block: str | None = None
    challenge: str | None = None
    vendor: str | None = None
    hint: str | None = None
    untried: str | None = None
    untried_reason: str | None = None
    hops: str | None = None
    ladder_truncated: str | None = None
    truncated: str | None = None
    network_truncated: str | None = None
    compact_truncated: str | None = None
    document: str | None = None
    document_units: int | None = None
    document_truncated: str | None = None
    usage_warning: str | None = None
    cache: str | None = None


def header_name(field: str) -> str:
    words = "-".join(w.capitalize() for w in field.split("_"))
    plain = ("cache_control", "content_security_policy", "referrer_policy")
    return words if field in plain else f"X-{words}"


@dataclasses.dataclass(frozen=True)
class Result:
    status: int
    content: bytes
    headers: Headers

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")


class MegalaniaError(Exception):
    def __init__(self, status: int, code: str | None, message: str, field: str | None,
                 request_id: str | None, report_url: str | None, headers: Headers = Headers()):
        super().__init__(message)
        self.headers = headers
        self.status = status
        self.code = code
        self.message = message
        self.field = field
        self.request_id = request_id
        self.report_url = report_url


class Megalania:
    def __init__(self, api_key: str | None = None, base_url: str = "https://get.megalania.io",
                 api_url: str = "https://api.megalania.io", timeout: float = 100.0):
        api_key = api_key or os.environ.get("MEG_API_KEY")
        if not api_key:
            raise ValueError("no API key: pass api_key or set MEG_API_KEY")
        self._timeout = timeout
        self.base_url = base_url
        self.api_url = api_url
        auth = {"Authorization": f"Bearer {api_key}"}
        self._http = httpx.Client(base_url=base_url, headers=auth, timeout=httpx.Timeout(timeout))
        self._api = httpx.Client(base_url=api_url, headers=auth, timeout=httpx.Timeout(timeout))

    def __repr__(self) -> str:
        return f"Megalania(base_url={self.base_url!r}, api_url={self.api_url!r})"

    def __enter__(self) -> "Megalania":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()
        self._api.close()

    def _send(self, http: httpx.Client, method: str, path: str, *, idempotency_key: str | None = None,
              create: bool = False, **kw: Any) -> httpx.Response:
        if create or idempotency_key:
            kw["headers"] = {"Idempotency-Key": idempotency_key or str(uuid.uuid4())}
        r = http.request(method, path, **kw)
        if r.status_code == 429:
            after = r.headers.get("retry-after")
            wait = 1 if after is None else _int(after)
            if wait is not None and 0 <= wait <= 60:
                time.sleep(wait)
                r = http.request(method, path, **kw)
        if r.status_code >= 400:
            raise _error(r)
        return r

    def _json(self, http: httpx.Client, method: str, path: str, **kw: Any) -> Any:
        r = self._send(http, method, path, **kw)
        return r.json() if r.content else None

    def scrape(self, url: str, *, idempotency_key: str | None = None, **params: Any) -> Result:
        r = self._send(self._http, "POST", "/v1", idempotency_key=idempotency_key, create=True,
                       json={"url": url, **_envelope(params)})
        return Result(r.status_code, r.content, _headers(r.headers))

    def get_tier(self, host: str, **query: Any) -> dict:
        return self._json(self._http, "GET", "/v1/tier", params={"host": host, **query})

    def get_domain_stats(self, host: str, **query: Any) -> dict:
        return self._json(self._http, "GET", "/v1/stats/domain", params={"host": host, **query})

    def get_account(self) -> dict:
        return self._json(self._api, "GET", "/v1/account")

    def get_usage(self, **query: Any) -> dict:
        return self._json(self._api, "GET", "/v1/account/usage", params=query)

    def rotate_webhook_secret(self) -> dict:
        return self._json(self._api, "POST", "/v1/account/webhook-secret/rotate")

    def map_site(self, url: str, *, idempotency_key: str | None = None, **params: Any) -> dict:
        return self._json(self._http, "POST", "/v1/map", idempotency_key=idempotency_key, create=True,
                          json={"url": url, **params})

    def create_batch(self, urls: list[str], *, idempotency_key: str | None = None, **params: Any) -> dict:
        return self._json(self._api, "POST", "/v1/batches", idempotency_key=idempotency_key, create=True,
                          json={"urls": urls, **_envelope(params)})

    def quote_batch(self, urls: list[str], **params: Any) -> dict:
        return self._json(self._api, "POST", "/v1/batches/quote", json={"urls": urls, **_envelope(params)})

    def list_batches(self, **query: Any) -> dict:
        return self._json(self._api, "GET", "/v1/batches", params=query)

    def get_batch(self, id: str) -> dict:
        return self._json(self._api, "GET", f"/v1/batches/{_id(id)}")

    def list_batch_items(self, id: str, **query: Any) -> dict:
        return self._json(self._api, "GET", f"/v1/batches/{_id(id)}/items", params=query)

    def cancel_batch(self, id: str) -> dict:
        return self._json(self._api, "POST", f"/v1/batches/{_id(id)}/cancel")

    def create_monitor(self, *, idempotency_key: str | None = None, **body: Any) -> dict:
        return self._json(self._api, "POST", "/v1/monitors", idempotency_key=idempotency_key, create=True,
                          json=body)

    def list_monitors(self, **query: Any) -> dict:
        return self._json(self._api, "GET", "/v1/monitors", params=query)

    def get_monitor(self, id: str) -> dict:
        return self._json(self._api, "GET", f"/v1/monitors/{_id(id)}")

    def update_monitor(self, id: str, **body: Any) -> dict:
        return self._json(self._api, "PATCH", f"/v1/monitors/{_id(id)}", json=body)

    def delete_monitor(self, id: str) -> None:
        self._json(self._api, "DELETE", f"/v1/monitors/{_id(id)}")

    def run_monitor(self, id: str) -> dict:
        return self._json(self._api, "POST", f"/v1/monitors/{_id(id)}/run")

    def list_monitor_checks(self, id: str, **query: Any) -> dict:
        return self._json(self._api, "GET", f"/v1/monitors/{_id(id)}/checks", params=query)

    def wait_batch(self, id: str, *, timeout: float = 3600.0, poll: float = 2.0) -> dict:
        end = time.monotonic() + timeout
        while True:
            batch = self.get_batch(id)
            if batch.get("status") in ("done", "failed", "canceled"):
                return batch
            if time.monotonic() + poll > end:
                raise TimeoutError(f"batch {id} still {batch.get('status')} after {timeout:g} s")
            time.sleep(poll)

    def read_results(self, items: list[dict]) -> list[bytes]:
        links = [item["result_url"] for item in items if item.get("result_url")]
        if not links:
            return []

        def get(link: str) -> bytes:
            r = plain.get(link)
            if r.status_code >= 400:
                raise _error(r)
            return r.content

        with httpx.Client(timeout=httpx.Timeout(self._timeout)) as plain, \
                ThreadPoolExecutor(max_workers=min(8, len(links))) as pool:
            return list(pool.map(get, links))

    def batch_results(self, id: str) -> Iterator[tuple[dict, bytes]]:
        cursor = None
        while True:
            page = self.list_batch_items(id, limit=100, **({"cursor": cursor} if cursor else {}))
            items = [item for item in page.get("items") or [] if item.get("result_url")]
            yield from zip(items, self.read_results(items))
            cursor = page.get("next_cursor")
            if not cursor:
                return

    def read_pages(self, urls: str | list[str], *, crawl: dict | None = None, continue_on_failure: bool = False,
                   **params: Any) -> Iterator[tuple[str, dict]]:
        urls = [urls] if isinstance(urls, str) else list(urls)
        if crawl is not None:
            if len(urls) != 1:
                raise ValueError("a crawl starts from exactly one URL")
            batch = self.create_batch(urls, crawl=crawl, **{"response_types": _default_type(params), **params})
            self.wait_batch(batch["id"])
            for item, body in self.batch_results(batch["id"]):
                yield body.decode("utf-8", errors="replace"), {
                    "source": item.get("url"), "depth": item.get("depth"), "target_status": item.get("target_status")}
            return
        for url in urls:
            try:
                r = self.scrape(url, **{"response_types": _default_type(params), **params})
            except MegalaniaError as e:
                if not continue_on_failure:
                    raise
                logging.getLogger("megalania").warning("skipped a page: %s (request %s)", e.code, e.request_id)
                continue
            yield r.text, {"source": url, "request_id": r.headers.request_id,
                           "credits_charged": r.headers.credits_charged, "target_status": r.headers.target_status}


def _envelope(params: dict) -> dict:
    schema = params.get("schema")
    return params if schema is None or isinstance(schema, str) else {**params, "schema": json.dumps(schema)}


def _default_type(params: dict) -> str:
    return "json" if "schema" in params else "markdown"


def _id(v: str) -> str:
    return urllib.parse.quote(str(v), safe="")


def _int(v: str | None) -> int | None:
    try:
        return int(v) if v is not None else None
    except ValueError:
        return None


def _headers(h: httpx.Headers) -> Headers:
    values: dict[str, Any] = {}
    for f in dataclasses.fields(Headers):
        v = h.get(header_name(f.name))
        if v is not None:
            values[f.name] = _int(v) if int in typing.get_args(f.type) else v
    return Headers(**values)


def _error(r: httpx.Response) -> MegalaniaError:
    rid = r.headers.get("x-request-id")
    try:
        e = r.json()["error"]
        return MegalaniaError(r.status_code, e.get("code"), e.get("message") or r.text[:500], e.get("field"),
                              rid, e.get("report_url"), _headers(r.headers))
    except (ValueError, KeyError, TypeError, AttributeError):
        return MegalaniaError(r.status_code, None, r.text[:500] or f"HTTP {r.status_code}", None, rid, None,
                              _headers(r.headers))


__all__ = ["Headers", "Megalania", "MegalaniaError", "Result"]
