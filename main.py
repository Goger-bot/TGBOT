import telebot
from PIL import Image
from io import BytesIO
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

TOKEN = '7090120977:AAFhL9N0LxAWHAxdxOdqI8Muj7VtNW_ugP8'
bot = telebot.TeleBot(TOKEN)

# Загрузка обученной модели
model = load_model('model.h5')  # Замените на путь к вашему файлу .h5

# Обработчик команды start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне изображение, и я скажу, гепард это или слон.")

# Обработчик получения фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image = Image.open(BytesIO(downloaded_file))
    image = image.resize((150, 150))
    image_array = img_to_array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)
    label = 'Слон' if prediction[0][0] > 0.5 else 'Гепард'

    bot.reply_to(message, f'Это похоже на {label}!')

print("Бот готов к работе!")
# Запуск бота
bot.polling()