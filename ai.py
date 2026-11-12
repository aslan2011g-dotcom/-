import asyncio
import os
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, WEBAPP_URL
from data import WORDS
from ai import explain

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📖 Открыть словарь", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await m.answer("Привет! Открывай словарь 👇", reply_markup=kb)

# --- КРОШЕЧНЫЙ ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle_root(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render сам дает порт в переменную PORT
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

# --- ЗАПУСК ---
async def main():
    # Запускаем веб-сервер в фоне (чтобы Render видел порт)
    asyncio.create_task(start_web_server())
    # Запускаем самого бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
