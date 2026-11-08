import json
import os
import unittest
from unittest import mock

from fakeapi import FakeApi
from langchain_megalania import TOOLS, MegalaniaLoader, megalania_tools
from megalania import Megalania, MegalaniaError

ID = "0199a1c2-0000-7000-8000-000000000001"
OK = {"X-Credits-Charged": "1", "X-Request-Id": "r1", "X-Target-Status": "200"}


def client(api: FakeApi) -> Megalania:
    return Megalania("k", base_url=api.url, api_url=api.url)


def by_name(api: FakeApi, **kw):
    return {t.name: t for t in megalania_tools(client=client(api), **kw)}


class LangChain(unittest.TestCase):
    def test_loader_scrape_documents(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# A", **OK)
            docs = MegalaniaLoader(["https://a.test/", "https://b.test/"], client=client(api)).load()
            self.assertEqual([d.page_content for d in docs], ["# A", "# A"])
            self.assertEqual(docs[1].metadata, {"source": "https://b.test/", "request_id": "r1", "credits_charged": 1, "target_status": 200})

    def test_loader_schema_asks_for_json_and_returns_it(self):
        schema = {"type": "object", "additionalProperties": False, "properties": {"title": {"type": "string"}}}
        with FakeApi() as api:
            api.add("POST", "/v1", body='{"data": {"title": "A"}}', **OK)
            docs = MegalaniaLoader("https://a.test/", schema=schema, client=client(api)).load()
            self.assertEqual(docs[0].page_content, '{"data": {"title": "A"}}')
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "response_types": "json", "schema": json.dumps(schema)})

    def test_loader_blocked_raises(self):
        with FakeApi() as api:
            api.error("POST", "/v1", 422, "blocked")
            with self.assertRaises(MegalaniaError) as c:
                MegalaniaLoader("https://a.test/", client=client(api)).load()
            self.assertEqual(c.exception.code, "blocked")

    def test_loader_continue_on_failure(self):
        with FakeApi() as api:
            api.error("POST", "/v1", 422, "blocked").add("POST", "/v1", body="# B", **OK)
            docs = MegalaniaLoader(["https://a.test/", "https://b.test/"], continue_on_failure=True, client=client(api)).load()
            self.assertEqual([d.metadata["source"] for d in docs], ["https://b.test/"])

    def test_loader_crawl_uses_batch(self):
        with FakeApi() as api:
            api.add("POST", "/v1/batches", body={"id": ID, "status": "queued"})
            api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": "done"})
            api.add("GET", f"/v1/batches/{ID}/items", body={"items": [{"url": "https://a.test/", "depth": 0, "target_status": 200, "result_url": f"{api.url}/r/1"}]})
            api.add("GET", "/r/1", body="<h1>A</h1>")
            docs = MegalaniaLoader("https://a.test/", crawl={"max_pages": 5}, client=client(api)).load()
            self.assertEqual([(d.page_content, d.metadata["depth"]) for d in docs], [("<h1>A</h1>", 0)])

    def test_tools_names_and_schema(self):
        with FakeApi() as api:
            tools = megalania_tools(client=client(api))
            self.assertEqual([t.name for t in tools], ["scrape", "extract", "map_site", "create_batch", "get_batch"])
            self.assertEqual(tools[0].args_schema, TOOLS[0]["inputSchema"])

    def test_extract_tool_asks_for_json_with_the_schema_and_the_cap(self):
        schema = {"type": "object", "additionalProperties": False, "properties": {"title": {"type": "string"}}}
        with FakeApi() as api:
            api.add("POST", "/v1", body='{"data": {"title": "A"}}', **OK)
            out = by_name(api)["extract"].invoke({"url": "https://a.test/", "schema": schema})
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "schema": json.dumps(schema), "response_types": "json", "max_credits": 128})
            self.assertTrue(out.startswith('{"data": {"title": "A"}}'))

    def test_tool_sends_default_max_credits_128(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# A", **OK).add("POST", "/v1/batches", body={"id": ID})
            t = by_name(api)
            out = t["scrape"].invoke({"url": "https://a.test/"})
            t["create_batch"].invoke({"urls": ["https://a.test/"]})
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "response_types": "markdown", "max_credits": 128})
            self.assertEqual(api.calls[1]["body"]["max_credits"], 128)
            self.assertTrue(out.endswith("[credits_charged=1 request_id=r1]"))

    def test_tool_max_credits_override(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# A", **OK)
            by_name(api, max_credits=300)["scrape"].invoke({"url": "https://a.test/"})
            self.assertEqual(api.calls[0]["body"]["max_credits"], 300)

    def test_tool_truncates(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="x" * 50, **OK)
            out = by_name(api, max_chars=10)["scrape"].invoke({"url": "https://a.test/"})
            self.assertTrue(out.startswith("x" * 10 + "\n[truncated: 40 more characters]"))

    def test_tool_cut_note_on_x_truncated(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# A", **OK, **{"X-Truncated": "max_credits"})
            out = by_name(api)["scrape"].invoke({"url": "https://a.test/"})
            self.assertIn("[cut at max_credits=128: create the tools with a higher max_credits (up to 32767)", out)

    def test_tool_too_low_error_names_price(self):
        with FakeApi() as api:
            api.add("POST", "/v1", 400, {"error": {"code": "max_credits_too_low", "message": "the lowest price is 32"}})
            out = by_name(api, max_credits=8)["scrape"].invoke({"url": "https://a.test/"})
            self.assertIn("max_credits=8 is below the cheapest route", out)
            self.assertIn("the lowest price is 32", out)

    def test_create_batch_caps_pages(self):
        with FakeApi() as api:
            api.add("POST", "/v1/batches", body={"id": ID})
            t = by_name(api, max_pages=2)["create_batch"]
            out = t.invoke({"urls": ["https://a.test/1", "https://a.test/2", "https://a.test/3"]})
            self.assertIn("too_many_pages: 3 URLs is above max_pages=2", out)
            self.assertEqual(api.calls, [])
            t.invoke({"urls": ["https://a.test/"], "crawl": {"max_pages": 5000, "max_depth": 3}})
            t.invoke({"urls": ["https://a.test/"], "crawl": {}})
            self.assertEqual([c["body"]["crawl"] for c in api.calls], [{"max_pages": 2, "max_depth": 3}, {"max_pages": 2}])

    def test_get_batch_raises_on_an_expired_link(self):
        with FakeApi() as api:
            api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": "done"})
            api.add("GET", f"/v1/batches/{ID}/items", body={"items": [{"url": "https://a.test/", "status": "done", "result_url": f"{api.url}/r/1"}]})
            api.add("GET", "/r/1", 403, "expired")
            out = by_name(api)["get_batch"].invoke({"batch_id": ID})
            self.assertTrue(out.startswith("403:"), out)

    def test_get_batch_reads_content(self):
        with FakeApi() as api:
            api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": "done"})
            api.add("GET", f"/v1/batches/{ID}/items", body={"items": [{"url": "https://a.test/", "status": "done", "result_url": f"{api.url}/r/1"}], "next_cursor": None})
            api.add("GET", "/r/1", body="# A")
            out = by_name(api)["get_batch"].invoke({"batch_id": ID})
            self.assertIn('"content": "# A"', out)
            self.assertIn('"status": "done"', out)

    def test_no_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(ValueError, "MEG_API_KEY"):
            megalania_tools()


if __name__ == "__main__":
    unittest.main()
