import logging
from credentials import TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime
import asyncio

chat_ids = [137588396]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение и добавляет чат ID в список."""
    chat_id = update.message.chat_id
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
    await update.message.reply_text('Привет, я буду отправлять тебе уведомления по расписанию!')

async def send_notifications(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет уведомления всем подписанным чатам."""
    for chat_id in chat_ids:
        await context.bot.send_message(chat_id=chat_id, text="Это запланированное уведомление!")

def schedule_jobs(application) -> None:
    """Функция для планирования уведомлений."""
    job_queue = application.job_queue
    job_queue.run_daily(
        send_notifications,
        time=datetime.time(hour=9, minute=0, second=0),
        name="daily_notification"
    )

def main() -> None:
    """Запускает бота."""
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    schedule_jobs(application)

    application.run_polling()

if __name__ == '__main__':
    main()
