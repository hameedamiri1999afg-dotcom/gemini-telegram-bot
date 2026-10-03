import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

from google import genai

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN تنظیم نشده است.")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY تنظیم نشده است.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message or not update.message.text:
        return

    user_message = update.message.text

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=user_message
        )

        answer = response.text

        if not answer:
            answer = "نتوانستم پاسخی دریافت کنم."

        await update.message.reply_text(answer)

    except Exception as e:
        logging.error("Gemini error: %s", e)
        await update.message.reply_text(
            "خطایی هنگام دریافت پاسخ از Gemini رخ داد."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("HZR Gemini Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
