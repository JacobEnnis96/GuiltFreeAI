#Simple python server script for handling hosting, model download requests, and web search for GuiltFreeAI.
#Will add gunicorn support when hosting to larger audience
import json
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
#Non-production port for testing. Fetty Wap.
PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GuiltFreeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # cross-origin isolation: required for SharedArrayBuffer, which wllama
        # needs to run inference on multiple cpu threads. jsdelivr serves the
        # needed CORP header on the wasm/esm imports, so require-corp is safe.
        # credentialless allows cross-origin fetches (e.g. HuggingFace) without
        # the remote server sending CORP headers, but it is not supported in
        # Firefox or Safari.
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/search":
            self.handle_search(parse_qs(parsed.query))
        else:
            super().do_GET()

    def handle_search(self, params):
        query = (params.get("q", [""])[0] or "").strip()
        if not query:
            self.send_json(400, {"error": "Missing query parameter 'q'"})
            return

        try:
            results = DDGS().text(query, max_results=5)
            self.send_json(200, results)
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def send_json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[server] {self.address_string()} - {fmt % args}")

if __name__ == "__main__":
    print(f"GuiltFreeAI server running at http://localhost:{PORT}")
    ThreadingHTTPServer(("", PORT), GuiltFreeHandler).serve_forever()
