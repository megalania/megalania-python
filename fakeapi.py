import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class FakeApi:
    def __init__(self):
        self.routes: dict[tuple[str, str], list[tuple[int, object, dict]]] = {}
        self.calls: list[dict] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def handle_one(self):
                n = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(n) if n else b""
                url = urllib.parse.urlsplit(self.path)
                fake.calls.append({"method": self.command, "path": url.path,
                                   "query": dict(urllib.parse.parse_qsl(url.query)),
                                   "auth": self.headers.get("Authorization"),
                                   "body": json.loads(raw) if raw else None})
                answers = fake.routes.get((self.command, url.path)) or [(404, {"error": {"code": "not_found", "message": "no route"}}, {})]
                status, body, headers = answers.pop(0) if len(answers) > 1 else answers[0]
                headers = dict(headers)
                data = body if isinstance(body, bytes) else (body.encode() if isinstance(body, str) else json.dumps(body).encode())
                self.send_response(status)
                self.send_header("Content-Type", headers.pop("Content-Type", "text/markdown" if isinstance(body, (str, bytes)) else "application/json"))
                for k, v in headers.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            do_GET = do_POST = do_PATCH = do_DELETE = handle_one

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def add(self, method: str, path: str, status: int = 200, body: object = None, **headers: str) -> "FakeApi":
        self.routes.setdefault((method, path), []).append((status, {} if body is None else body, dict(headers)))
        return self

    def error(self, method: str, path: str, status: int, code: str, **headers: str) -> "FakeApi":
        return self.add(method, path, status, {"error": {"code": code, "message": f"fake {code}"}},
                        **{"X-Request-Id": "r-err", **headers})

    def __enter__(self) -> "FakeApi":
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.server.shutdown()
        self.server.server_close()
