import asyncio
import json
import os
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, WEBAPP_URL
from ai import explain

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📖 Открыть словарь", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await m.answer("Привет! Это интерактивный словарь Happy House.\nОткрывай Mini App 👇", reply_markup=kb)

# --- БОТ ЛОВИТ ДАННЫЕ ОТ САЙТА И ОТВЕЧАЕТ В ЧАТ ---
@dp.message(F.web_app_data)
async def on_webapp_data(m: Message):
    try:
        data = json.loads(m.web_app_data.data)
        term = data.get("term")
        definition = data.get("def")
    except:
        await m.answer("Ошибка чтения данных от сайта.")
        return

    msg = await m.answer("⏳ Думаю...")
    # Вызываем нашего локального ИИ
    text = explain(term, definition)
    
    await msg.edit_text(
        f"<b>{term}</b>\n\n<i>{definition}</i>\n\n{text}\n\n"
        "<i>Сгенерировано AI, могут быть неточности</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="⬅️ Назад в словарь", web_app=WebAppInfo(url=WEBAPP_URL))
        ]])
    )

# --- ЗАГЛУШКА ДЛЯ RENDER (чтобы он не перезапускал бота) ---
async def handle_root(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
