import telebot
import os
import logging
from data import token_tg_b, id_chat
from telebot import types
from database import save_story, get_stories, delete_story
from adv_check import check_advertising_text

os.system('cls')

bot = telebot.TeleBot(token_tg_b)
# logging.basicConfig(level=logging.DEBUG)

@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.type == 'private':
        user_id = m.from_user.id
        user_first_name = str(m.chat.first_name)
        last_name = str(m.chat.last_name)
        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'Инкогнито'

        bot.send_message(m.chat.id, text=f'''
Привееет, <b>{user_first_name} {last_name}</b>, делись с нами своими историями
А другие тебя поддержат!
Будь добрее)
''', parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=["suggest_a_post"])
def suggest_a_post(message: types.Message):
    global user_first_name, last_name
    user_id = message.from_user.id
    user_first_name = str(message.chat.first_name) 
    last_name = str(message.chat.last_name)
    if last_name == 'None':
            last_name = ''
    if user_first_name == 'None':
        user_first_name = 'No Name'

    if message.chat.type == 'private':
        if message.content_type != 'text':
            # Если получено сообщение с вложением, отправляем уведомление
            bot.send_message(message.from_user.id, "Извини, но нельзя отправлять сообщения с вложениями(")
        else:
            bot.send_message(message.from_user.id, '''
            Отправь мне свою историю и я отправлю это в канал)\n\n---------------------------------------
<b>! WARNING !</b>\n
1. Редактировать текст после отправки <b>НЕВОЗМОЖНО</b>, поэтому желательно подумать и потом прислать мне.\n
2. <b>ЗАПРЕЩАЕТСЯ</b> отправлять текст с вложениями!
            ''', parse_mode='html')
            bot.register_next_step_handler(message, process_post)


def process_post(message: types.Message):
    user_id = message.from_user.id
    story_text = message.text


    if check_advertising_text(story_text) is False:
        if story_text is not None:
            if not "/" in story_text:
            
                save_story(user_id, story_text)  # Сохраняем историю в базе данных
            else: # Если сообщение содержит символ "/", отправляем уведомление о запрете команд
                bot.send_message(message.from_user.id, "Извини, но нельзя отправлять команды/ссылки(\n\nПовтори вызов команды и снова отправь свою историю")
        else: 
            bot.send_message(message.from_user.id, 'Незя присылать вложения!')
    else:
        bot.send_video(message.from_user.id, video='BAACAgIAAxkBAAICNWR6SK5IK8te9q4qFTVa5DWC5flTAALqMgACZr7ZS98yLje7RuTwLwQ', caption=f'Ну вот ты и попался, {user_first_name + last_name}\n\nНезя так')
        

def publish_stories():
    stories = get_stories()  # Получаем все истории из базы данных

    for story in stories:
        if not story.sent:
            bot.send_message(id_chat, story.story_text)
            bot.send_message(story.user_id, "Твоя история отправлена на публикацию)")

            story.sent = True
            delete_story(story.user_id, story.story_text)  # Удалить историю по её ID, а не по user_id и story_text

            break  # Прервать цикл после удаления истории


if __name__ == '__main__':
    publish_stories()  # Выполняем функцию publish_stories в одном потоке
    bot.polling(none_stop=True)
