import json
import os
import unittest
from unittest import mock

from fakeapi import FakeApi
from megalania import Megalania, MegalaniaError

ID = "0199a1c2-0000-7000-8000-000000000001"


def client(api: FakeApi) -> Megalania:
    return Megalania("k", base_url=api.url, api_url=api.url)


class Composites(unittest.TestCase):
    def test_wait_batch_returns_on_terminal(self):
        with FakeApi() as api:
            for s in ("queued", "running", "done"):
                api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": s})
            self.assertEqual(client(api).wait_batch(ID, poll=0.01)["status"], "done")
            self.assertEqual(len(api.calls), 3)

    def test_wait_batch_times_out(self):
        with FakeApi() as api:
            api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": "running"})
            with self.assertRaises(TimeoutError):
                client(api).wait_batch(ID, timeout=0.05, poll=0.01)

    def test_batch_results_skips_items_without_link_and_pages(self):
        with FakeApi() as api:
            path = f"/v1/batches/{ID}/items"
            api.add("GET", path, body={"items": [{"id": "a", "result_url": f"{api.url}/r/a"}, {"id": "b", "result_url": None}], "next_cursor": "c2"})
            api.add("GET", path, body={"items": [{"id": "c", "result_url": f"{api.url}/r/c"}], "next_cursor": None})
            api.add("GET", "/r/a", body="A").add("GET", "/r/c", body="C")
            got = list(client(api).batch_results(ID))
            self.assertEqual([(i["id"], b) for i, b in got], [("a", b"A"), ("c", b"C")])
            self.assertEqual(api.calls[2]["query"]["cursor"], "c2")
            self.assertEqual([c["auth"] for c in api.calls if c["path"].startswith("/r/")], [None, None])

    def test_read_results_keeps_order_and_raises_on_a_bad_link(self):
        with FakeApi() as api:
            for n in range(10):
                api.add("GET", f"/r/{n}", body=str(n))
            items = [{"result_url": f"{api.url}/r/{n}"} for n in range(10)] + [{"result_url": None}]
            self.assertEqual(client(api).read_results(items), [str(n).encode() for n in range(10)])
            api.add("GET", "/r/gone", 403, "expired")
            with self.assertRaises(MegalaniaError) as c:
                client(api).read_results([{"result_url": f"{api.url}/r/gone"}])
            self.assertEqual(c.exception.status, 403)

    def test_read_pages_crawl_yields_finished_items_of_a_failed_batch(self):
        with FakeApi() as api:
            api.add("POST", "/v1/batches", body={"id": ID, "status": "queued"})
            api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": "failed"})
            api.add("GET", f"/v1/batches/{ID}/items", body={"items": [
                {"id": "a", "url": "https://megalania.io/", "depth": 0, "target_status": 200, "result_url": f"{api.url}/r/a"},
                {"id": "b", "url": "https://megalania.io/x", "depth": 1, "target_status": None, "result_url": None}]})
            api.add("GET", "/r/a", body="<h1>A</h1>")
            pages = list(client(api).read_pages("https://megalania.io/", crawl={"max_pages": 2}))
            self.assertEqual(pages, [("<h1>A</h1>", {"source": "https://megalania.io/", "depth": 0, "target_status": 200})])
            self.assertEqual(api.calls[0]["body"], {"urls": ["https://megalania.io/"], "crawl": {"max_pages": 2}, "response_types": "markdown"})

    def test_read_pages_crawl_needs_one_url(self):
        with FakeApi() as api, self.assertRaises(ValueError):
            list(client(api).read_pages(["https://a.test/", "https://b.test/"], crawl={}))

    def test_read_pages_blocked_raises_or_skips(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# ok", **{"X-Credits-Charged": "1", "X-Request-Id": "r1", "X-Target-Status": "200"})
            with self.assertRaises(MegalaniaError) as c:
                api.routes[("POST", "/v1")].insert(0, (422, {"error": {"code": "blocked", "message": "b"}}, {}))
                list(client(api).read_pages(["https://a.test/", "https://b.test/"]))
            self.assertEqual(c.exception.code, "blocked")
            api.routes[("POST", "/v1")].insert(0, (422, {"error": {"code": "blocked", "message": "b"}}, {}))
            with self.assertLogs("megalania") as logs:
                pages = list(client(api).read_pages(["https://a.test/", "https://b.test/"], continue_on_failure=True))
            self.assertEqual(pages, [("# ok", {"source": "https://b.test/", "request_id": "r1", "credits_charged": 1, "target_status": 200})])
            self.assertNotIn("a.test", "".join(logs.output))
            self.assertEqual(api.calls[-1]["body"], {"url": "https://b.test/", "response_types": "markdown"})

    def test_envelope_numbers_are_sent_as_numbers(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# ok").add("POST", "/v1/batches", body={"id": ID})
            client(api).scrape("https://a.test/", max_credits=128, timeout=30, network=True)
            client(api).create_batch(["https://a.test/"], max_credits=64, crawl={"max_pages": 5})
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "max_credits": 128, "timeout": 30, "network": True})
            self.assertEqual(api.calls[1]["body"], {"urls": ["https://a.test/"], "max_credits": 64, "crawl": {"max_pages": 5}})

    def test_schema_goes_as_json_text_and_read_pages_then_asks_for_json(self):
        schema = {"type": "object", "additionalProperties": False, "properties": {"title": {"type": "string"}}}
        with FakeApi() as api:
            api.add("POST", "/v1", body='{"data": {"title": "A"}}').add("POST", "/v1/batches", body={"id": ID})
            pages = list(client(api).read_pages("https://a.test/", schema=schema, prompt="the title"))
            client(api).create_batch(["https://a.test/"], schema='{"type":"object"}', response_types="json")
            self.assertEqual(pages[0][0], '{"data": {"title": "A"}}')
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "response_types": "json", "schema": json.dumps(schema), "prompt": "the title"})
            self.assertEqual(api.calls[1]["body"]["schema"], '{"type":"object"}')

    def test_account_usage_stats_and_webhook_secret(self):
        with FakeApi() as api:
            api.add("GET", "/v1/account", body={"balance": 5}).add("GET", "/v1/account/usage", body={"usage": []})
            api.add("GET", "/v1/stats/domain", body={"requests": 0}).add("POST", "/v1/account/webhook-secret/rotate", body={"secret": "s"})
            meg = client(api)
            self.assertEqual(meg.get_account(), {"balance": 5})
            self.assertEqual(meg.get_usage(days=7), {"usage": []})
            self.assertEqual(meg.get_domain_stats("a.test", days=30), {"requests": 0})
            self.assertEqual(meg.rotate_webhook_secret(), {"secret": "s"})
            self.assertEqual([(c["method"], c["path"], c["query"]) for c in api.calls], [
                ("GET", "/v1/account", {}), ("GET", "/v1/account/usage", {"days": "7"}),
                ("GET", "/v1/stats/domain", {"host": "a.test", "days": "30"}), ("POST", "/v1/account/webhook-secret/rotate", {})])

    def test_key_from_env_or_value_error(self):
        with mock.patch.dict(os.environ, {"MEG_API_KEY": "from-env"}):
            self.assertIsNotNone(Megalania())
        with mock.patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(ValueError, "MEG_API_KEY"):
            Megalania()


if __name__ == "__main__":
    unittest.main()
