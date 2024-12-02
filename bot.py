import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
AVAL_AI_API_TOKEN = os.getenv('AVAL_AI_API_TOKEN')

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    base_url="https://api.avalai.ir/v1",
    api_key=AVAL_AI_API_TOKEN
)

def query_langchain_ai(message: str) -> str:
    try:
        response = llm.invoke(message)
        if hasattr(response, "content"):
            return response.content
        else:
            return str(response)
    except Exception as e:
        return f"خطا در ارتباط با سرور هوش مصنوعی: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! من ربات چت جی‌پی‌تی هستم.\n"
        "این پروژه به عنوان بخشی از یک پروژه دانشجویی توسعه داده شده است.\n"
        "برای شروع، پیام خود را تایپ کنید و من سعی می‌کنم به بهترین شکل ممکن به شما پاسخ دهم. 😊"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = query_langchain_ai(user_message)
    await update.message.reply_text(response)

def main():
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    application.run_polling()

if __name__ == '__main__':
    main()