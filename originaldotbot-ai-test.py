import logging
from aiogram import Bot, Dispatcher, executor, types
from transformers import pipeline
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.__version__)
print("Is CUDA available (GPU support)?", torch.cuda.is_available())


# Конфігурація логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
API_TOKEN = '7157883595:AAG9rR9ovslnfeIciHQncSkqvCiSznIjVfI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Завантаження моделі для аналізу настроїв
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Обробник команди /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Надішліть мені текст, і я проаналізую його настрій.")

# Обробник для текстових повідомлень
@dp.message_handler(content_types=types.ContentType.TEXT)
async def analyze_sentiment(message: types.Message):
    user_text = message.text
    result = sentiment_model(user_text)
    await message.reply(f"Настрій: {result[0]['label']}, Впевненість: {result[0]['score']:.2f}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
