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


# =========================
# Logging
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================
# Environment Variables
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN تنظیم نشده است.")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY تنظیم نشده است.")


# =========================
# Gemini
# =========================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODEL = "gemini-2.5-flash"


# =========================
# Telegram Message Handler
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    if not update.message.text:
        return

    user_message = update.message.text.strip()

    if not user_message:
        return

    try:
        logger.info("User message: %s", user_message)

        response = client.models.generate_content(
            model=MODEL,
            contents=user_message
        )

        answer = response.text

        if not answer:
            answer = "Gemini پاسخی برنگرداند."

        logger.info("Gemini response received.")

        await update.message.reply_text(answer)

    except Exception as e:
        logger.exception("Gemini error")

        await update.message.reply_text(
            "خطایی در Gemini رخ داد.\n\n"
            f"نوع خطا: {type(e).__name__}\n"
            f"جزئیات: {str(e)}"
        )


# =========================
# Start Bot
# =========================

def main():

    logger.info("Starting HZR Gemini Bot...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    logger.info("HZR Gemini Bot is running...")

    app.run_polling()


# =========================
# Run
# =========================

if __name__ == "__main__":
    main()
