import os
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

DB_FILE = "aravali_content.db"  # your SQLite database

# --- DB search ---
def search_db(query):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT c.title, c.link
        FROM content_search s
        JOIN content c ON s.rowid = c.id
        WHERE s.plain_text MATCH ?
        LIMIT 5
    """, (query,)).fetchall()
    conn.close()
    return rows

# --- /search command ---
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /search <keyword>")
        return

    query = " ".join(context.args)
    results = search_db(query)

    if results:
        reply = "\n\n".join([f"📌 {title}\n{link}" for title, link in results])
    else:
        reply = "No results found."
    await update.message.reply_text(reply)

# --- /start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Use /search <keyword> to query Aravali Education content.")

# --- Main ---
def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # read token from environment
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set in environment variables!")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
