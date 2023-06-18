import telebot
from data import t_token_tg_b, t_id_att

bot = telebot.TeleBot(t_token_tg_b)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Отправьте мне медиагруппу, и я перешлю её в чат.")




cou = []  # Переменная для хранения списка file_id

@bot.message_handler(content_types=['video'])
def handle_media_group(message):
    print(message)
    file_id = message.video.file_id
    cou.append(file_id)

    
    if len(cou) <= 10:  # Если набрано достаточное количество вложений
        media_group = [telebot.types.InputMedia(file_id) for file_id in cou]
        bot.send_media_group(t_id_att, media=media_group)
        cou.clear()  # Очистка списка

    

def main():
    bot.polling()

if __name__ == "__main__":
    main()
