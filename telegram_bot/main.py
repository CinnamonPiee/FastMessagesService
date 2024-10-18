import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart


logging.basicConfig(level=logging.INFO)
bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для уведомлений.")


async def send_notification(user_id: int, text: str):
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"User with id {user_id} sent you a message:\n{text}"
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
