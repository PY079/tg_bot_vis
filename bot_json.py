import telebot
from data import token_tg_b, id_chat

bot = telebot.TeleBot(token_tg_b)
@bot.message_handler(content_types=['photo','video','audio','document'])
def handle_text(message):
    if message.photo:
        # Обработка фото
        photo = message.photo[-1]  # Получаем самое крупное фото из доступных размеров
        file_id = photo.file_id  # Идентификатор файла фото
        file_unique_id = photo.file_unique_id  # Уникальный идентификатор файла фото
        file_size = photo.file_size  # Размер файла фото
        bot.send_photo(id_chat ,caption=f'тест photo\n{message.caption}', photo=file_id)
        # Ваш код обработки фото

    elif message.video:
        # Обработка видео
        video = message.video
        file_id = video.file_id
        file_unique_id = video.file_unique_id
        file_size = video.file_size
        bot.send_video(id_chat ,caption=f'тест video\n{message.caption}', video=file_id)

        # Ваш код обработки видео

    elif message.audio:
        # Обработка аудио
        audio = message.audio
        file_id = audio.file_id
        file_unique_id = audio.file_unique_id
        file_size = audio.file_size
        bot.send_audio(id_chat ,caption=f'тест audio\n{message.caption}', audio=file_id)

        # Ваш код обработки аудио

    elif message.document:
        # Обработка документа
        document = message.document
        file_id = document.file_id
        file_unique_id = document.file_unique_id
        file_size = document.file_size
        bot.send_document(id_chat ,caption=f'тест document\n{message.caption}', document=file_id)
        # Ваш код обработки документа
    print(file_id)
    



bot.polling(non_stop=True)


