import contextlib
import io
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

from fakeapi import FakeApi
from megalania import Megalania, cli

ID = "0199a1c2-0000-7000-8000-000000000001"


def run(api: FakeApi | None, *argv: str, key: str | None = "k", stdin: str = "") -> tuple[int, str, str]:
    env = {"MEG_API_KEY": key} if key else {}
    out, err = io.StringIO(), io.StringIO()
    out.buffer = io.BytesIO()
    factory = (lambda: Megalania("k", base_url=api.url, api_url=api.url)) if api else cli.client_factory
    with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(cli, "client_factory", factory), \
            mock.patch("sys.stdin", io.StringIO(stdin)), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(list(argv))
    return code, out.getvalue() + out.buffer.getvalue().decode(), err.getvalue()


class Cli(unittest.TestCase):
    def test_scrape_writes_body(self):
        with FakeApi() as api:
            api.add("POST", "/v1", body="# A", **{"X-Credits-Charged": "1", "X-Request-Id": "r1"})
            code, out, err = run(api, "scrape", "https://a.test/", "--max-credits", "64", "--response-types", "markdown")
            self.assertEqual((code, out), (0, "# A"))
            self.assertIn("credits_charged=1", err)
            self.assertEqual(api.calls[0]["body"], {"url": "https://a.test/", "response_types": "markdown", "max_credits": 64})

    def test_no_key_exits_2(self):
        code, _, err = run(None, "scrape", "https://a.test/", key=None)
        self.assertEqual((code, err.strip()), (2, "megalania: no API key: pass api_key or set MEG_API_KEY"))

    def test_plain_http_host_is_refused_except_localhost(self):
        with mock.patch.dict(os.environ, {"MEG_API_KEY": "k", "MEG_BASE_URL": "http://get.example.test"}, clear=True), \
                contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(cli.main(["scrape", "https://a.test/"]), 2)
        self.assertIn("MEG_BASE_URL must be an https URL", err.getvalue())
        with mock.patch.dict(os.environ, {"MEG_API_KEY": "k", "MEG_BASE_URL": "http://127.0.0.1:9"}, clear=True):
            self.assertEqual(cli.client_factory().base_url, "http://127.0.0.1:9")

    def test_batch_results_refuses_unsafe_item_ids(self):
        for bad in ("../x", "a/b", ".."):
            with FakeApi() as api, tempfile.TemporaryDirectory() as d:
                api.add("GET", f"/v1/batches/{ID}/items", body={"items": [{"id": bad, "result_url": f"{api.url}/r/1"}]})
                api.add("GET", "/r/1", body="# A")
                code, _, err = run(api, "batch", "results", ID, "--dir", d)
                self.assertEqual(code, 2, bad)
                self.assertIn("not a safe file name", err)
                self.assertEqual(os.listdir(d), [])

    def test_api_error_exits_1_without_url(self):
        with FakeApi() as api:
            api.error("POST", "/v1", 422, "blocked")
            code, _, err = run(api, "scrape", "https://secret.test/page")
            self.assertEqual(code, 1)
            self.assertEqual(err.strip(), "error blocked: fake blocked (request r-err)")

    def test_batch_results_names_files_by_item_id(self):
        with FakeApi() as api, tempfile.TemporaryDirectory() as d:
            api.add("GET", f"/v1/batches/{ID}/items", body={"items": [{"id": "i1", "url": "https://a.test/x", "result_url": f"{api.url}/r/1"}]})
            api.add("GET", "/r/1", body="# A")
            code, _, _ = run(api, "batch", "results", ID, "--dir", d)
            self.assertEqual((code, os.listdir(d)), (0, ["i1"]))
            self.assertEqual(pathlib.Path(d, "i1").read_text(), "# A")

    def test_json_merges_under_flags(self):
        with FakeApi() as api:
            api.add("POST", "/v1/batches", body={"id": ID})
            code, out, _ = run(api, "batch", "create", "https://a.test/", "--crawl", '{"max_pages": 5}', "--json", "-",
                               stdin='{"name": "n", "max_credits": "1"}', )
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["id"], ID)
            self.assertEqual(api.calls[0]["body"], {"urls": ["https://a.test/"], "name": "n", "max_credits": "1", "crawl": {"max_pages": 5}})

    def test_tier_is_get_tier(self):
        with FakeApi() as api:
            api.add("GET", "/v1/tier", body={"host": "a.test"})
            code, out, _ = run(api, "tier", "a.test")
            self.assertEqual((code, json.loads(out)), (0, {"host": "a.test"}))
            self.assertEqual(api.calls[0]["query"], {"host": "a.test"})

    def test_no_api_key_flag(self):
        with self.assertRaises(SystemExit) as c, contextlib.redirect_stderr(io.StringIO()):
            cli.main(["--api-key", "x", "scrape", "https://a.test/"])
        self.assertEqual(c.exception.code, 2)

    def test_skill_install_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(None, "skill", "install", "--dir", d, key=None)[0], 0)
            skill = pathlib.Path(d, "megalania", "SKILL.md")
            self.assertTrue(skill.read_text().startswith("---\nname: megalania\n"))
            skill.write_text("mine")
            self.assertEqual(run(None, "skill", "install", "--dir", d, key=None)[0], 2)
            self.assertEqual(run(None, "skill", "install", "--dir", d, "--force", key=None)[0], 0)


if __name__ == "__main__":
    unittest.main()
