from data import t_token_tg_b, t_id_channel
from telebot import types
import telebot
import chardet

def check_encoding(text, expected_encoding):
    encoded_text = text.encode()
    detected_encoding = chardet.detect(encoded_text)['encoding']
    return detected_encoding == expected_encoding






me = '''

Доброе время суток, ребятки!)
Можно вас попросить оценить, что-то по типу небольшого стихотворения от меня..? 👉👈

  Ɜнᴀᴇɯь, ᴛы - ᴄᴀʍᴏᴇ ᴧучɯᴇᴇ, чᴛᴏ быᴧᴏ ᴄᴏ ʍнᴏй. ᴛы ᴨᴇᴩʙᴀя, ᴨᴩᴀʙдᴀ, ᴛы ᴨᴇᴩʙᴀя, ᴋᴏʍу я, ᴏᴛᴋᴩыᴧᴄя ɜᴀᴋᴩыᴛыʍи ᴦᴧᴀɜᴀʍи и чиᴄᴛᴏй дуɯᴏй. Я ᴏчᴇнь ᴧюбᴧю ᴛᴇбя. Дᴀ я ᴏчᴇнь, я ᴏчᴇнь ᴧюбᴧю ᴛᴇбя.. 
Я хᴏчу быᴛь ᴄ ᴛᴏбᴏй дᴏ ᴨᴏᴛᴇᴩи ᴨуᴧьᴄᴀ
Я хᴏчу быᴛь ᴄ ᴛᴏбᴏй ᴋᴀждую ᴄᴇᴋунду, ʍинуᴛу, чᴀᴄ, дᴇнь, ᴋᴀждыᴇ ᴄуᴛᴋи и нᴇ ᴏᴛᴨуᴄᴋᴀᴛь ᴛᴇбя ниᴋᴏʍу, хᴏчу быᴛь ᴛᴏᴧьᴋᴏ ᴄ ᴛᴏбᴏй. ᴛы ʍᴏй чᴇᴧᴏʙᴇᴋ.. ᴄ ᴛᴏбᴏй ʍнᴇ ᴏчᴇнь ᴋᴏʍɸᴏᴩᴛнᴏ, ʍᴏя ᴧюбᴏʙь.💓🫶🏻

Вот оно.. Буду рада, честному критикованию.)'''

bot = telebot.TeleBot(t_token_tg_b)



@bot.message_handler(commands=["start"],content_types=['text'])
def suggest_a_post(message: types.Message):
    global user_first_name, last_name
    user_id = message.from_user.id
    user_first_name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    # Проверка имени пользователя на наличие только букв и цифр

    if last_name == 'None':
        last_name = ''
    if user_first_name == 'None':
        user_first_name = 'No Name'

    if message.chat.type == 'private':
        
        bot.send_message(message.from_user.id, '''
            тест''', parse_mode='html')
        bot.register_next_step_handler(message, process_post)


def process_post(message: types.Message):
    user_id = message.from_user.id
    story_text = message.text

    user_first_name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    # Проверка имени пользователя на наличие только букв и цифр

    if last_name == 'None':
        last_name = ''
    if user_first_name == 'None':
        user_first_name = 'No Name'

    # bot.send_message(message.from_user.id,message.text.casefold())
    if check_encoding(message.text, 'windows-1251'):
        bot.send_message(message.from_user.id, message.text)
    else:
        bot.send_message(message.from_user.id,"Кодировка не соответствует ожидаемой (Windows-1251)")
    # bot.send_message(message.from_user.id, message.text.encode('Windows-1251',errors=))

bot.polling(non_stop=True)