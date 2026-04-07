from telethon import TelegramClient, events
import asyncio
import re
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 🔑 פרטים מ-Render (ENV)
api_id = "39189498"
api_hash = "f457cf80ff6f8123dba1492bc4cf25ca"
bot_token = "8696135908:AAH81vCUOCTH6UGXPS7hlAjEpBr3b1dIMuA"

client = TelegramClient("bot", api_id, api_hash)

source_channel = "pkpoi"
target_channel = "@itay_alerts"

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    text = event.message.text or ""

    # ❌ מוחק פרסומות
    if "הישארו מעודכנים" in text:
        text = text.split("הישארו מעודכנים")[0]

    # 🧼 ניקוי טקסט
    text = re.sub(r'[*_`]', '', text)
    text = text.replace("❗", "").strip()

    if not text and not event.message.media:
        return

    final_text = f"{text}\n\n🔴 חדשות רק אמת בטלגרם 🔴\nhttps://t.me/itay_alerts"

    try:
        if event.message.media:
            await client.send_file(
                target_channel,
                event.message.media,
                caption=final_text,
                link_preview=False
            )
        else:
            await client.send_message(
                target_channel,
                final_text,
                link_preview=False
            )
    except Exception as e:
        print("❌ שגיאה:", e)


# 🔥 טריק ל-Render (פורט)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


async def main():
    await client.start(bot_token=bot_token)
    print("🚀 הבוט עובד!")
    await client.run_until_disconnected()


if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    asyncio.run(main())