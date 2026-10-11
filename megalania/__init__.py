import dataclasses
import time
import typing
import uuid
from typing import Any

import httpx


@dataclasses.dataclass(frozen=True)
class Headers:
    request_id: str | None = None
    cache_control: str | None = None
    credits_charged: int | None = None
    engine: str | None = None
    target_status: int | None = None
    timing_target_ms: int | None = None
    route: str | None = None
    identity: str | None = None
    billing: str | None = None
    block: str | None = None
    challenge: str | None = None
    vendor: str | None = None
    hint: str | None = None
    untried: str | None = None
    hops: str | None = None
    ladder_truncated: str | None = None
    truncated: str | None = None
    network_truncated: str | None = None
    compact_truncated: str | None = None
    usage_warning: str | None = None


def header_name(field: str) -> str:
    words = "-".join(w.capitalize() for w in field.split("_"))
    return words if field == "cache_control" else f"X-{words}"


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
    def __init__(self, api_key: str, base_url: str = "https://get.megalania.io", timeout: float = 100.0):
        self.base_url = base_url
        self._http = httpx.Client(base_url=base_url, headers={"Authorization": f"Bearer {api_key}"},
                                  timeout=httpx.Timeout(timeout))

    def __repr__(self) -> str:
        return f"Megalania(base_url={self.base_url!r})"

    def __enter__(self) -> "Megalania":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()

    def render(self, url: str, *, idempotency_key: str | None = None, **params: Any) -> Result:
        http = self._http
        headers = {"Idempotency-Key": idempotency_key or str(uuid.uuid4())}
        body = {"url": url, **params}
        r = http.post("/v1", json=body, headers=headers)
        if r.status_code == 429:
            after = r.headers.get("retry-after")
            wait = 1 if after is None else _int(after)
            if wait is not None and 0 <= wait <= 60:
                time.sleep(wait)
                r = http.post("/v1", json=body, headers=headers)
        if r.status_code >= 400:
            raise _error(r)
        return Result(r.status_code, r.content, _headers(r.headers))


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
