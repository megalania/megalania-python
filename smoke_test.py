import json
import os
import pathlib
import threading
import time
import unittest
from dataclasses import fields
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from megalania import Headers, Megalania, MegalaniaError, header_name

LIVE = os.environ.get("MEG_BASE_URL")
KEY = os.environ["MEG_API_KEY"] if LIVE else "test-key"
TARGET = os.environ["MEG_TARGET_URL"] if LIVE else "https://a.test/"
SEEN: list[dict] = []
DOC = pathlib.Path(__file__).resolve().parents[2] / "api/openapi/v1.yaml"


class Mock(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, body, ctype, **headers):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        for k, v in headers.items():
            self.send_header(k.replace("_", "-"), v)
        self.end_headers()
        self.wfile.write(body.encode())

    def error(self, status, code, field=None, **headers):
        body = {"error": {"code": code, "message": f"mock {code}", "report_url": "https://app.megalania.io/report"}}
        if field:
            body["error"]["field"] = field
        self.send(status, json.dumps(body), "application/json", X_Request_Id="r-err", **headers)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.append({"auth": self.headers["Authorization"], "key": self.headers["Idempotency-Key"], "body": body})
        path = body["url"].removeprefix("https://a.test")
        if self.headers["Authorization"] != "Bearer test-key":
            return self.error(401, "bad_token")
        if body.get("engine") == "nope":
            return self.error(400, "bad_parameter", "engine")
        if path == "/busy" or (path == "/once" and len(SEEN) == 1):
            return self.error(429, "over_concurrency", Retry_After="1")
        if path == "/long":
            return self.error(429, "over_concurrency", Retry_After="120")
        if path == "/dated":
            return self.error(429, "over_concurrency", Retry_After="Wed, 21 Oct 2026 07:28:00 GMT")
        if path == "/badnum":
            return self.send(200, "<p>ok</p>", "text/html", X_Request_Id="r1", X_Credits_Charged="abc")
        if path == "/down":
            return self.error(503, "busy", Retry_After="1")
        if path == "/edge":
            return self.send(500, "edge page", "text/plain")
        if path == "/blocked":
            return self.error(422, "blocked", X_Billing="blocked", X_Untried="c:dc,h:mob", X_Hops="h:dc:chrome=9",
                              X_Vendor="cloudflare")
        self.send(200, "<p>ok</p>", "text/html", X_Request_Id="r1", X_Credits_Charged="1", X_Engine="http",
                  X_Target_Status="200", X_Route="http/datacenter")


class Smoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = LIVE
        if not LIVE:
            cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Mock)
            threading.Thread(target=cls.server.serve_forever, daemon=True).start()
            cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        if not LIVE:
            cls.server.shutdown()

    def setUp(self):
        SEEN.clear()

    def client(self, key=KEY):
        return Megalania(key, base_url=self.base)

    def test_render(self):
        r = self.client().render(TARGET)
        self.assertTrue(r.text)
        self.assertIsInstance(r.headers.credits_charged, int)
        self.assertIsInstance(r.headers.request_id, str)
        if not LIVE:
            self.assertEqual([(s["auth"], s["body"]) for s in SEEN], [("Bearer test-key", {"url": TARGET})])

    def test_401(self):
        with self.assertRaises(MegalaniaError) as c:
            self.client("not-a-key").render(TARGET)
        self.assertEqual((c.exception.status, c.exception.code), (401, "bad_token"))

    def test_a_block_is_a_typed_free_422_and_never_retried(self):
        SEEN.clear()
        with self.assertRaises(MegalaniaError) as c:
            self.client().render("https://a.test/blocked")
        e = c.exception
        self.assertEqual((e.status, e.code, len(SEEN)), (422, "blocked", 1))
        self.assertEqual((e.headers.billing, e.headers.untried, e.headers.hops, e.headers.vendor),
                         ("blocked", "c:dc,h:mob", "h:dc:chrome=9", "cloudflare"))

    def test_400_typed(self):
        with self.assertRaises(MegalaniaError) as c:
            self.client().render(TARGET, engine="nope")
        e = c.exception
        self.assertEqual((e.status, e.code, e.field), (400, "bad_parameter", "engine"))
        self.assertTrue(e.message)
        self.assertTrue(e.request_id)

    @unittest.skipIf(LIVE, "mock only")
    def test_429_retried_once_after_retry_after(self):
        t = time.monotonic()
        self.assertEqual(self.client().render("https://a.test/once").status, 200)
        self.assertEqual(len(SEEN), 2)
        self.assertGreaterEqual(time.monotonic() - t, 1)

    @unittest.skipIf(LIVE, "mock only")
    def test_retry_reuses_the_idempotency_key(self):
        self.client().render("https://a.test/once")
        self.assertTrue(SEEN[0]["key"])
        self.assertEqual(SEEN[0]["key"], SEEN[1]["key"])

    @unittest.skipIf(LIVE, "mock only")
    def test_each_render_has_its_own_key(self):
        self.client().render(TARGET)
        self.client().render(TARGET)
        self.client().render(TARGET, idempotency_key="mine-1")
        self.assertEqual(len({s["key"] for s in SEEN}), 3)
        self.assertEqual(SEEN[2]["key"], "mine-1")

    @unittest.skipIf(LIVE, "mock only")
    def test_retry_after_above_60_is_an_error_without_sleep(self):
        t = time.monotonic()
        with self.assertRaises(MegalaniaError) as c:
            self.client().render("https://a.test/long")
        self.assertEqual((c.exception.status, len(SEEN)), (429, 1))
        self.assertLess(time.monotonic() - t, 1)

    @unittest.skipIf(LIVE, "mock only")
    def test_retry_after_date_is_an_error_without_retry(self):
        with self.assertRaises(MegalaniaError) as c:
            self.client().render("https://a.test/dated")
        self.assertEqual((c.exception.status, len(SEEN)), (429, 1))

    def test_key_not_in_repr(self):
        m = Megalania("test-key-" + "q" * 43, base_url=self.base)
        for _ in range(2):
            self.assertNotIn("q" * 43, repr(m) + repr(vars(m)))
            try:
                m.render(TARGET)
            except MegalaniaError:
                pass
        self.assertEqual(repr(m), f"Megalania(base_url={self.base!r})")

    @unittest.skipIf(LIVE, "mock only")
    def test_bad_numeric_header_is_none(self):
        r = self.client().render("https://a.test/badnum")
        self.assertIsNone(r.headers.credits_charged)
        self.assertEqual(r.headers.request_id, "r1")

    @unittest.skipIf(LIVE, "mock only")
    def test_second_429_is_an_error(self):
        with self.assertRaises(MegalaniaError) as c:
            self.client().render("https://a.test/busy")
        self.assertEqual(c.exception.code, "over_concurrency")
        self.assertEqual(len(SEEN), 2)

    @unittest.skipIf(LIVE, "mock only")
    def test_503_never_retried(self):
        with self.assertRaises(MegalaniaError) as c:
            self.client().render("https://a.test/down")
        self.assertEqual(c.exception.code, "busy")
        self.assertEqual(len(SEEN), 1)

    @unittest.skipIf(LIVE, "mock only")
    def test_error_body_not_json(self):
        with self.assertRaises(MegalaniaError) as c:
            self.client().render("https://a.test/edge")
        self.assertEqual((c.exception.status, c.exception.code, c.exception.message), (500, None, "edge page"))

    @unittest.skipUnless(DOC.exists(), "needs the platform OpenAPI document")
    def test_headers_match_the_document(self):
        from ruamel.yaml import YAML
        doc = YAML(typ="safe").load(DOC)
        documented = set(doc["components"]["responses"]["Scraped"]["headers"])
        self.assertEqual({header_name(f.name) for f in fields(Headers)}, documented)


if __name__ == "__main__":
    unittest.main()
