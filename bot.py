import asyncio
import json
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
    await m.answer(
        "Привет! Это интерактивный словарь Happy House (2026-2027).\n"
        "Открывай Mini App — там все слова с пояснениями от ИИ.",
        reply_markup=kb,
    )

# Запрос пояснения из WebApp
@dp.callback_query(F.data.startswith("explain:"))
async def cb_explain(cb: CallbackQuery):
    idx = int(cb.data.split(":")[1])
    w = WORDS[idx]
    await cb.message.edit_text("⏳ Думаю…")
    try:
        text = await explain(w["term"], w["def"])
    except Exception as e:
        text = f"Не удалось получить пояснение: {e}"
    await cb.message.edit_text(
        f"<b>{w['term']}</b>\n\n<i>{w['def']}</i>\n\n{text}\n\n"
        "<i>Сгенерировано AI, могут быть неточности</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="⬅️ Назад в словарь", web_app=WebAppInfo(url=WEBAPP_URL))
        ]]),
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
