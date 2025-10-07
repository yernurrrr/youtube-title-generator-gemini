import streamlit as st
import os
from google import genai # Используем библиотеку Google GenAI
from google.genai.errors import APIError # Для обработки ошибок

# --- КОНФИГУРАЦИЯ API И МОДЕЛИ ---
# Лучше всего хранить ключ в переменной окружения
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

def generate_titles(prompt_text):
    """Отправляет запрос к модели Gemini и возвращает сгенерированные заголовки."""
    if not GEMINI_API_KEY:
        return "Ошибка: Не найден GEMINI_API_KEY. Пожалуйста, установите переменную окружения."

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Инструкции (системный промпт), которые делают модель "экспертом"
    system_instruction = "Ты эксперт по созданию привлекательных и кликабельных заголовков для YouTube-видео. Отвечай только списком из 5 уникальных вариантов, не добавляя лишнего текста."

    # Пользовательский промпт
    full_prompt = (
        f"Сгенерируй 5 вариантов заголовков для YouTube-видео на основе следующей темы: '{prompt_text}'"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config={"system_instruction": system_instruction}
        )
        return response.text
    except APIError as e:
        return f"Произошла ошибка API: {e}"
    except Exception as e:
        return f"Произошла непредвиденная ошибка: {e}"

# --- ОСНОВНАЯ ЛОГИКА STREAMLIT ---

st.title("🔥 Генератор заголовков для YouTube (MVP)")
text_input = st.text_input("Введите тему вашего видео:", placeholder="Как быстро выучить Python", key="topic")

if st.button("Сгенерировать 🚀"):
    if text_input:
        st.info("Генерация... Это может занять несколько секунд.")

        # Вызов нашей функции
        result_text = generate_titles(text_input)

        # Отображение результата
        st.success("✅ Готово! Ваши заголовки:")
        st.markdown(result_text)

    else:
        st.warning("Пожалуйста, введите текст для генерации заголовка")
