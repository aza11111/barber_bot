import os
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in .env")
if ADMIN_ID == 0:
    raise RuntimeError("ADMIN_ID is not set in .env")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📅 Записаться"))
main_menu.add(KeyboardButton("💈 Цены"))
main_menu.add(KeyboardButton("📍 Адрес"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в Barbershop 💈\nВыберите действие:",
        reply_markup=main_menu
    )

@dp.message_handler(lambda m: m.text == "💈 Цены")
async def prices(message: types.Message):
    await message.answer("Стрижка — 100 000 сум\nБорода — 50 000 сум")

@dp.message_handler(lambda m: m.text == "📍 Адрес")
async def address(message: types.Message):
    await message.answer("📍 г. Ташкент, ул. Пример 10")

@dp.message_handler(lambda m: m.text == "📅 Записаться")
async def booking(message: types.Message):
    await message.answer("Напишите: Имя + время\nПример: Aziz 18:00")

@dp.message_handler()
async def save_booking(message: types.Message):
    # Отправляем админу
    username = message.from_user.username
    who = f"@{username}" if username else f"id:{message.from_user.id}"

    await bot.send_message(
        ADMIN_ID,
        f"💈 Новая запись!\n"
        f"Данные: {message.text}\n"
        f"От: {who}"
    )

    await message.answer("✅ Спасибо! Запись принята. Мы свяжемся с вами.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)