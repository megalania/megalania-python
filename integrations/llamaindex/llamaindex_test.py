import json
import os
import unittest
from unittest import mock

from fakeapi import FakeApi
from llama_index.readers.megalania import MegalaniaReader
from megalania import MegalaniaError

ID = "0199a1c2-0000-7000-8000-000000000001"
OK = {"X-Credits-Charged": "1", "X-Request-Id": "r1", "X-Target-Status": "200"}


def reader(api: FakeApi, **kw) -> MegalaniaReader:
    return MegalaniaReader(api_key="k", base_url=api.url, api_url=api.url, **kw)


class LlamaIndex(unittest.TestCase):
    def test_reader_scrape(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# A", **OK)
            docs = reader(api).load_data(["https://a.test/"])
            self.assertEqual([(d.text, d.metadata["source"]) for d in docs], [("# A", "https://a.test/")])

    def test_reader_schema_asks_for_json_and_returns_it(self):
        schema = {"type": "object", "additionalProperties": False, "properties": {"title": {"type": "string"}}}
        with FakeApi() as api:
            api.add("POST", "/v1", body='{"data": {"title": "A"}}', **OK)
            docs = reader(api).load_data("https://a.test/", schema=schema)
            self.assertEqual(docs[0].text, '{"data": {"title": "A"}}')
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "response_types": "json", "schema": json.dumps(schema)})

    def test_reader_crawl(self):
        with FakeApi() as api:
            api.add("POST", "/v1/batches", body={"id": ID, "status": "queued"})
            api.add("GET", f"/v1/batches/{ID}", body={"id": ID, "status": "done"})
            api.add("GET", f"/v1/batches/{ID}/items", body={"items": [{"url": "https://a.test/", "depth": 0, "target_status": 200, "result_url": f"{api.url}/r/1"}]})
            api.add("GET", "/r/1", body="<h1>A</h1>")
            docs = reader(api).load_data("https://a.test/", crawl={})
            self.assertEqual([d.text for d in docs], ["<h1>A</h1>"])

    def test_reader_continue_on_failure(self):
        with FakeApi() as api:
            api.error("POST", "/v1", 422, "blocked")
            with self.assertRaises(MegalaniaError):
                reader(api).load_data(["https://a.test/"])
            api.routes.clear()
            api.error("POST", "/v1", 422, "blocked").add("POST", "/v1", body="# B", **OK)
            docs = reader(api, continue_on_failure=True).load_data(["https://a.test/", "https://b.test/"])
            self.assertEqual([d.metadata["source"] for d in docs], ["https://b.test/"])

    def test_key_never_leaves_the_reader(self):
        r = MegalaniaReader(api_key="do-not-leak-7f3a")
        for text in (repr(r), str(r), r.to_json(), json.dumps(r.to_dict()), r.model_dump_json()):
            self.assertNotIn("do-not-leak-7f3a", text)

    def test_no_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(ValueError, "MEG_API_KEY"):
            MegalaniaReader().load_data(["https://a.test/"])


if __name__ == "__main__":
    unittest.main()
