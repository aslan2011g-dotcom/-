import os
from groq import AsyncGroq
from dotenv import load_dotenv

# Загружаем переменные из файла .env (если он есть)
load_dotenv()

# Берем ключ из настроек. НИ В КОЕМ СЛУЧАЕ не пиши ключ прямо сюда!
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "Ты — толкователь внутреннего сленга школьного сообщества «Happy House» (сезон 2026-2027). "
    "Тебе дают слово и официальное краткое толкование из их словаря. "
    "Твоя задача — дать живое, дружелюбное пояснение на русском (3-6 предложений): "
    "что это значит, в каком контексте употребляется, какие ассоциации/шутки могут быть. "
    "Не выдумывай факты, которых нет; если данных мало — так и скажи. "
    "Пиши с лёгким юмором, но без грубости."
)

async def explain(term: str, definition: str) -> str:
    try:
        response = await client.chat.completions.create(
            # Бесплатная и мощная модель
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Слово: {term}\nОфициальное толкование: {definition}\n\nПоясни подробнее."},
            ],
            temperature=0.7,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка при запросе к ИИ: {e}"
