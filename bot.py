import asyncio
import json
import os
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, WEBAPP_URL
from ai import explain # Наша новая функция пояснений

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📖 Открыть словарь", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await m.answer("Привет! Открывай словарь 👇", reply_markup=kb)

# --- ВОТ ЭТОТ БЛОК ЛОВИТ ДАННЫЕ ОТ САЙТА ---
@dp.message(F.web_app_data)
async def on_webapp_data(m: Message):
    try:
        data = json.loads(m.web_app_data.data)
        term = data.get("term")
        definition = data.get("def")
    except Exception as e:
        await m.answer(f"Ошибка чтения данных: {e}")
        return

    # Отправляем "Думаю..."
    msg = await m.answer("⏳ Думаю...")
    
    # Получаем текст от нашего локального ИИ (из ai.py)
    text = explain(term, definition)
    
    # Меняем сообщение на ответ
    await msg.edit_text(
        f"<b>{term}</b>\n\n<i>{definition}</i>\n\n{text}\n\n"
        "<i>Сгенерировано AI, могут быть неточности</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="⬅️ Назад в словарь", web_app=WebAppInfo(url=WEBAPP_URL))
        ]])
    )

# --- ВЕБ-СЕРВЕР (чтобы Render не перезапускал бота) ---
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
