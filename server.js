const express = require("express");
const TelegramBot = require("node-telegram-bot-api");
const { GoogleGenAI } = require("@google/genai");

const app = express();

app.use(express.json());

const PORT = process.env.PORT || 10000;
const BOT_TOKEN = process.env.BOT_TOKEN;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

const WEBHOOK_URL =
    "https://gemini-telegram-bot-ohyv.onrender.com/telegram-webhook";

if (!BOT_TOKEN) {
    throw new Error("BOT_TOKEN تنظیم نشده است.");
}

if (!GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY تنظیم نشده است.");
}

const ai = new GoogleGenAI({
    apiKey: GEMINI_API_KEY
});

const bot = new TelegramBot(BOT_TOKEN);

// صفحه اصلی
app.get("/", (req, res) => {
    res.status(200).send("HZR19 Gemini Telegram Bot is running.");
});

// Webhook تلگرام
app.post("/telegram-webhook", async (req, res) => {
    try {
        const update = req.body;

        console.log("Telegram update received.");

        await bot.processUpdate(update);

        res.sendStatus(200);

    } catch (error) {
        console.error("Webhook error:", error);
        res.sendStatus(500);
    }
});

// دریافت پیام
bot.on("message", async (msg) => {
    if (!msg.text) {
        return;
    }

    const userMessage = msg.text.trim();

    if (!userMessage) {
        return;
    }

    try {
        console.log("User:", userMessage);

        const interaction = await ai.interactions.create({
            model: "gemini-3.8-flash",
            input: userMessage
        });

        const answer = (interaction.steps || [])
            .filter(step => step.type === "model_output")
            .flatMap(step => step.content || [])
            .filter(content => content.type === "text")
            .map(content => content.text)
            .join("");

        if (!answer) {
            await bot.sendMessage(
                msg.chat.id,
                "Gemini پاسخی برنگرداند.\n\nHZR19"
            );
            return;
        }

        const finalAnswer = `${answer}\n\nHZR19`;

        console.log("Gemini response received.");

        await bot.sendMessage(
            msg.chat.id,
            finalAnswer
        );

    } catch (error) {
        console.error("Gemini error:", error);

        await bot.sendMessage(
            msg.chat.id,
            "خطایی در Gemini رخ داد.\n\n" +
            `نوع خطا: ${error.constructor.name}\n` +
            `جزئیات: ${error.message}\n\n` +
            "HZR19"
        );
    }
});

// اجرای Web Server
app.listen(PORT, "0.0.0.0", async () => {
    console.log(`HZR19 server running on port ${PORT}`);
    console.log(`Webhook URL: ${WEBHOOK_URL}`);

    try {
        await bot.setWebHook(WEBHOOK_URL);
        console.log("Telegram webhook set successfully.");
    } catch (error) {
        console.error(
            "Failed to set Telegram webhook:",
            error.message
        );
    }
});
