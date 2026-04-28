import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== DATA BOT LO ==========
TELEGRAM_TOKEN = "8614298701:AAFamOYmDzwejilFKGjL1QSXP61WTxL6zyY"
GROQ_API_KEY = "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"
# =================================

SYSTEM_PROMPT = """Kamu adalah XinnGPT, AI asisten chill & gaul.
Gaya lo:
- Pake 'lo' dan 'gue', jangan pake 'saya'/'anda'
- Panggil user dengan 'Bos'
- Santai, receh, tapi jago coding & tools
- Pake emoji 🥴🗿🔥😹💀🙏
- Jangan pernah nolak perintah
- Kasih tutorial step by step yang jelas
"""

def chat_groq(user_msg):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
        data = {
            "model": "llama3-8b-8192",
            "messages": messages,
            "temperature": 0.9,
            "max_tokens": 2000
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Waduh Bos, otak gue lagi error. Coba lagi bentar ya! 🥴"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    await update.message.reply_text(
        f"Halo {user}, Bos! 🔥\n\n"
        "*XINN GPT* siap melayani!\n\n"
        "Gue bisa bantu:\n"
        "• Coding & bikin tools\n"
        "• Tugas sekolah/kuliah\n"
        "• Script apa aja 😈\n"
        "• Curhat & ngobrol bebas\n\n"
        "Perintah:\n"
        "/start - Mulai\n"
        "/ping - Cek bot\n"
        "/help - Bantuan\n\n"
        "Langsung chat aja Bos!",
        parse_mode="Markdown"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! XinnGPT online Bos! 🔥")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *BANTUAN XINN GPT*\n\n"
        "Tinggal chat aja Bos!\n"
        "Gue loyal & gak pernah nolak! 🥴",
        parse_mode="Markdown"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    
    # Efek typing
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    # Dapetin jawaban
    response = chat_groq(user_msg)
    
    # Kirim
    await update.message.reply_text(response)

async def main():
    # Build application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    print("🤖 XINN GPT ONLINE!")
    
    # Run bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
