import json
import pathlib
from collections.abc import Callable, Iterator
from typing import Any

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.tools import StructuredTool, ToolException
from megalania import Megalania, MegalaniaError

TOOLS: list[dict] = json.loads((pathlib.Path(__file__).parent / "tools.json").read_text())


class MegalaniaLoader(BaseLoader):
    def __init__(self, urls: str | list[str], *, api_key: str | None = None, crawl: dict | None = None,
                 continue_on_failure: bool = False, client: Megalania | None = None, **params: Any):
        self.client = client or Megalania(api_key)
        self.urls = urls
        self.crawl = crawl
        self.continue_on_failure = continue_on_failure
        self.params = params

    def lazy_load(self) -> Iterator[Document]:
        for text, meta in self.client.read_pages(self.urls, crawl=self.crawl,
                                                 continue_on_failure=self.continue_on_failure, **self.params):
            yield Document(page_content=text, metadata=meta)


def cut(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}\n[truncated: {len(text) - max_chars} more characters]"


def explain(e: MegalaniaError, max_credits: int) -> str:
    if e.code == "max_credits_too_low":
        return (f"max_credits_too_low: max_credits={max_credits} is below the cheapest route for this page. "
                f"Create the tools with a higher max_credits (up to 32767). {e.message}")
    return f"{e.code or e.status}: {e.message}"


def megalania_tools(api_key: str | None = None, *, max_credits: int = 128, max_pages: int = 100,
                    max_chars: int = 100_000, client: Megalania | None = None) -> list[StructuredTool]:
    meg = client or Megalania(api_key)

    def scrape(url: str, **kw: Any) -> str:
        r = meg.scrape(url, **{"response_types": "markdown", **kw, "max_credits": max_credits})
        text = cut(r.text, max_chars)
        if r.headers.truncated == "max_credits":
            text += (f"\n[cut at max_credits={max_credits}: create the tools with a higher max_credits "
                     f"(up to 32767) to get the whole page]")
        return f"{text}\n\n[credits_charged={r.headers.credits_charged} request_id={r.headers.request_id}]"

    def extract(url: str, **kw: Any) -> str:
        r = meg.scrape(url, **{**kw, "response_types": "json", "max_credits": max_credits})
        return f"{cut(r.text, max_chars)}\n\n[credits_charged={r.headers.credits_charged} request_id={r.headers.request_id}]"

    def map_site(url: str, **kw: Any) -> str:
        return json.dumps(meg.map_site(url, **kw))

    def create_batch(urls: list[str], crawl: dict | None = None, **kw: Any) -> str:
        if len(urls) > max_pages:
            raise ToolException(f"too_many_pages: {len(urls)} URLs is above max_pages={max_pages}. "
                                f"Create the tools with a higher max_pages to send more in one batch.")
        if crawl is not None:
            crawl = {**crawl, "max_pages": min(int(crawl.get("max_pages") or max_pages), max_pages)}
            kw["crawl"] = crawl
        return json.dumps(meg.create_batch(urls, **{**kw, "max_credits": max_credits}))

    def get_batch(batch_id: str, cursor: str | None = None, limit: int = 20) -> str:
        batch = meg.get_batch(batch_id)
        page = meg.list_batch_items(batch_id, limit=limit, **({"cursor": cursor} if cursor else {}))
        items = page.get("items") or []
        share = max_chars // max(1, len(items))
        bodies = iter(meg.read_results(items))
        out = []
        for item in items:
            row = {k: item.get(k) for k in ("url", "status", "error", "credits_charged", "target_status")}
            if item.get("result_url"):
                row["content"] = cut(next(bodies).decode("utf-8", errors="replace"), share)
            out.append(row)
        return json.dumps({**batch, "items": out, "next_cursor": page.get("next_cursor")})

    def wrap(fn: Callable[..., str]) -> Callable[..., str]:
        def run(**kw: Any) -> str:
            try:
                return fn(**kw)
            except MegalaniaError as e:
                raise ToolException(explain(e, max_credits)) from e
        return run

    fns = {"scrape": scrape, "extract": extract, "map_site": map_site, "create_batch": create_batch, "get_batch": get_batch}
    return [StructuredTool.from_function(func=wrap(fns[t["name"]]), name=t["name"], description=t["description"],
                                         args_schema=t["inputSchema"], handle_tool_error=True) for t in TOOLS]


__all__ = ["MegalaniaLoader", "megalania_tools"]
