import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من HZR Bot هستم.\n"
        "ربات با موفقیت فعال شد."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستورات موجود:\n"
        "/start - شروع ربات\n"
        "/help - راهنما"
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN در Environment Variables تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("HZR Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
