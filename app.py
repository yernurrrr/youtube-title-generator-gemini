import streamlit as st
import os
from google import genai
from google.genai.errors import APIError

# --- КОНФИГУРАЦИЯ API И МОДЕЛИ ---
# Ключ GEMINI_API_KEY будет получен из Streamlit Secrets (или из локального окружения)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

def generate_titles(prompt_text, style):
    """Отправляет запрос к модели Gemini, включая выбранный стиль."""
    if not GEMINI_API_KEY:
        # Это сообщение покажется, если ключ не установлен в Streamlit Secrets или локально
        return "Ошибка: Не найден GEMINI_API_KEY. Пожалуйста, установите переменную окружения (на SCS или локально)."

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Инструкции (системный промпт), которые делают модель "экспертом"
    # *** ИСПОЛЬЗУЕМ ВЫБОР СТИЛЯ В ПРОМПТЕ ***
    system_instruction = (
        f"Ты эксперт по созданию привлекательных и кликабельных заголовков для YouTube-видео. Твой стиль должен быть: '{style}'. "
        "Отвечай только списком из 5 уникальных вариантов, не добавляя лишнего текста или комментариев."
    )

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

st.set_page_config(page_title="Генератор Заголовков", layout="centered")
st.title("🔥 Генератор заголовков для YouTube (MVP)")

# 1. Поле ввода темы
text_input = st.text_input("Введите тему вашего видео:", placeholder="Как быстро выучить Python", key="topic")

# 2. Поле выбора стиля (НОВЫЙ ЭЛЕМЕНТ)
style_selection = st.selectbox(
    "Выберите желаемый стиль заголовков:",
    options=["Информационный", "Кликбейтный (интригующий)", "Юмористический", "Серьезный"],
    key="style"
)

if st.button("Сгенерировать 🚀"):
    if text_input:
        st.info("Генерация... Это может занять несколько секунд.")

        # *** ПЕРЕДАЧА СТИЛЯ В ФУНКЦИЮ ***
        result_text = generate_titles(text_input, style_selection)

        # Отображение результата
        st.success("✅ Готово! Ваши заголовки:")
        st.markdown(result_text)

    else:
        st.warning("Пожалуйста, введите текст для генерации заголовка")
