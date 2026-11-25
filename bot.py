import os
import logging
import feedparser
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FEEDS = [
    "https://weworkremotely.com/categories/remote-design-jobs.rss",
    "https://remotive.com/remote-jobs/feed"
]

KEYWORDS = [
    "freelance", "freelancer", "contract", "commission",
    "3d modeling", "3d artist", "illustrator", "2d artist",
    "game artist", "animation", "children's book"
]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Freelance Lead Finder is ready. Use /scan to check for opportunities."
    )

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Checking public job feeds...")

    found = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            text = f"{title} {summary}".lower()

            if any(word in text for word in KEYWORDS):
                found.append(
                    f"📌 {title}\n{entry.get('link', '')}\n"
                    f"Use this as a lead to review before contacting the client."
                )

    if not found:
        await update.message.reply_text("No matching opportunities found in this scan.")
        return

    for item in found[:10]:
        await update.message.reply_text(item)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    app.run_polling()

if __name__ == "__main__":
    main()
