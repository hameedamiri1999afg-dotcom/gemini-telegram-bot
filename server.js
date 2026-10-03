const express = require("express");
const TelegramBot = require("node-telegram-bot-api");
const { GoogleGenAI } = require("@google/genai");

const app = express();

const PORT = process.env.PORT || 10000;
const BOT_TOKEN = process.env.BOT_TOKEN;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

if (!BOT_TOKEN) {
    throw new Error("BOT_TOKEN تنظیم نشده است.");
}

if (!GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY تنظیم نشده است.");
}

const ai = new GoogleGenAI({
    apiKey: GEMINI_API_KEY
});

const bot = new TelegramBot(BOT_TOKEN, {
    polling: true
});

app.get("/", (req, res) => {
    res.status(200).send("HZR Gemini Telegram Bot is running.");
});

bot.on("message", async (msg) => {
    if (!msg.text) return;

    const userMessage = msg.text.trim();

    if (!userMessage) return;

    try {
        console.log("User:", userMessage);

        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: userMessage
        });

        const answer = response.text;

        if (!answer) {
            await bot.sendMessage(
                msg.chat.id,
                "Gemini پاسخی برنگرداند."
            );
            return;
        }

        console.log("Gemini:", answer);

        await bot.sendMessage(
            msg.chat.id,
            answer
        );

    } catch (error) {
        console.error("Gemini error:", error);

        await bot.sendMessage(
            msg.chat.id,
            "خطایی هنگام دریافت پاسخ از Gemini رخ داد."
        );
    }
});

bot.on("polling_error", (error) => {
    console.error("Telegram polling error:", error.message);
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`HZR Gemini Bot server running on port ${PORT}`);
});
