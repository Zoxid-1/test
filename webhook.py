from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")


def redis_set(key, value):
    req = urllib.request.Request(
        f"{UPSTASH_URL}/set/{key}/{value}",
        headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"},
    )
    urllib.request.urlopen(req, timeout=8)


def telegram_api(method, payload):
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        pass


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"

        try:
            update = json.loads(body)
        except Exception:
            update = {}

        cq = update.get("callback_query")
        if cq:
            data = cq.get("data", "")
            cq_id = cq.get("id")
            message = cq.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            message_id = message.get("message_id")
            original_text = message.get("text", "")

            if ":" in data:
                action, app_id = data.split(":", 1)
                if action in ("approve", "reject") and UPSTASH_URL and UPSTASH_TOKEN:
                    status = "approved" if action == "approve" else "rejected"
                    try:
                        redis_set(app_id, status)
                    except Exception:
                        pass

                    label = "\n\n✅ TASDIQLANDI" if status == "approved" else "\n\n❌ RAD ETILDI"
                    if chat_id and message_id:
                        telegram_api("editMessageText", {
                            "chat_id": chat_id,
                            "message_id": message_id,
                            "text": original_text + label,
                        })

                    if cq_id:
                        telegram_api("answerCallbackQuery", {
                            "callback_query_id": cq_id,
                            "text": "Holat saqlandi",
                        })

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Webhook is alive. Set this URL as your Telegram bot webhook.")
