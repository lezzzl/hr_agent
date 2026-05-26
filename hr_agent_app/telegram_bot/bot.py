import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from hr_agent_app.service import finish_interview, handle_message

MAX_TELEGRAM_MESSAGE_LENGTH = 3900

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def split_long_message(text: str, max_length: int = MAX_TELEGRAM_MESSAGE_LENGTH) -> list[str]:
    if len(text) <= max_length:
        return [text]

    chunks: list[str] = []
    current = ""

    for paragraph in text.split("\n\n"):
        separator = "\n\n" if current else ""
        candidate = f"{current}{separator}{paragraph}"

        if len(candidate) <= max_length:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        while len(paragraph) > max_length:
            chunks.append(paragraph[:max_length])
            paragraph = paragraph[max_length:]

        current = paragraph

    if current:
        chunks.append(current)

    return chunks


async def send_text(update: Update, text: str) -> None:
    if update.effective_chat is None:
        return

    for chunk in split_long_message(text):
        await update.effective_chat.send_message(chunk)


def get_chat_id(update: Update) -> str:
    if update.effective_chat is None:
        raise RuntimeError("Telegram chat is missing in update.")

    return str(update.effective_chat.id)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context

    chat_id = get_chat_id(update)
    try:
        response = handle_message(chat_id, "Привет")
    except Exception:
        logger.exception("Failed to start HR agent conversation")
        response = "Произошла техническая ошибка при запуске интервью. Попробуйте ещё раз позже."

    await send_text(update, response)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context

    chat_id = get_chat_id(update)
    finish_interview(chat_id)
    await send_text(update, "Диалог сброшен. Напишите /start, чтобы начать заново.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context

    await send_text(
        update,
        "Я HR-бот для первичного интервью в ML-команду.\n\n"
        "Команды:\n"
        "/start - начать интервью\n"
        "/reset - сбросить текущий диалог\n"
        "/help - показать помощь\n\n"
        "Также можно задавать вопросы о процессе найма, ролях, формате работы и слотах интервью.",
    )


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context

    if update.message is None or update.message.text is None:
        return

    chat_id = get_chat_id(update)
    text = update.message.text.strip()
    if not text:
        return

    try:
        response = handle_message(chat_id, text)
    except Exception:
        logger.exception("Failed to handle Telegram message")
        response = "Произошла техническая ошибка. Попробуйте ещё раз позже."

    await send_text(update, response)


def build_application() -> Application:
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Add it to .env.")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    return application


def main() -> None:
    application = build_application()
    logger.info("Telegram HR agent bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
