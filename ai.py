from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=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)

SYSTEM = (
    "Ты — толкователь внутреннего сленга школьного сообщества «Happy House» (сезон 2026-2027). "
    "Тебе дают слово и официальное краткое толкование из их словаря. "
    "Твоя задача — дать живое, дружелюбное пояснение на русском (3-6 предложений): "
    "что это значит, в каком контексте употребляется, какие ассоциации/шутки могут быть. "
    "Не выдумывай факты, которых нет; если данных мало — так и скажи. "
    "Пиши с лёгким юмором, но без грубости."
)

async def explain(term: str, definition: str) -> str:
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Слово: {term}\nОфициальное толкование: {definition}\n\nПоясни подробнее."},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    return resp.choices[0].message.content.strip()
