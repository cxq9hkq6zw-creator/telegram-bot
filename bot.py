from telethon import TelegramClient, events
import asyncio
import re
import os

# 🔐 משתנים מ-Render (Environment Variables)
api_id = "39189498"
api_hash = "f457cf80ff6f8123dba1492bc4cf25ca"
bot_token = "8696135908:AAH81vCUOCTH6UGXPS7hlAjEpBr3b1dIMuA״

client = TelegramClient("session", api_id, api_hash)

source_channel = "pkpoi"
target_channel = "itay_alerts"

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    text = event.message.text or ""

    # ❌ מוחק פרסומות
    if "הישארו מעודכנים" in text:
        text = text.split("הישארו מעודכנים")[0]

    # 🧼 ניקוי טקסט
    text = re.sub(r'[*_`]', '', text)
    text = text.replace("❗", "").strip()

    # ✅ טקסט סופי
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

async def main():
    await client.start()
    print("🚀 הבוט עובד!")
    await client.run_until_disconnected()

asyncio.run(main())