import telebot
import os
import logging
from data import token_tg_b, id_channel, id_acc, id_chat_info
from telebot import types
from database import save_story, get_stories, delete_story
from adv_check import check_advertising_text
from send_message_datab import add_user, update_user_active_status, get_user





os.system('cls')

bot = telebot.TeleBot(token_tg_b)
# logging.basicConfig(level=logging.DEBUG)

@bot.message_handler(commands=['start'])
def start(m: types.Message):
    if m.chat.type == 'private':
        user_id = m.from_user.id
        add_user(user_id)
        user_first_name = str(m.chat.first_name)
        last_name = str(m.chat.last_name)
        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'Инкогнито'

        bot.send_message(m.chat.id, text=f'''
Привееет, <b>{user_first_name} {last_name}</b>, делись с нами своими историями
А другие тебя поддержат!
Будь добрее)\n\n
В данный момент бот написан на 100%. 
Если <b>возникают ошибки</b>, то пишите <a href='t.me//JKPyGtH'>сюда</a>\n
Бот создан разработчиком: <a href ='t.me//JKPyGtH'>PY079</a>
''', parse_mode='html', disable_web_page_preview=True)

@bot.message_handler(commands=['menu'])
def menu(m: types.Message):
    if m.chat.type == 'private':
        user_id = m.from_user.id
        bot.send_message(m.chat.id, text='''
<b>Меню:</b>
1. /start - Команда, которую можно использовать для начала общения с ботом. Она инициирует диалог с ботом и позволяет выполнить определенные действия.\n
2. /menu - Команда, которая выводит это меню. При ее выполнении бот отправит тебе список доступных команд.\n
3. /suggest_a_post -  Команда, которую можно использовать для отправки своей истории боту с целью ее публикации. Ты можешь поделиться своими переживаниями, историями успеха или любыми другими историями, которые хотели бы поделиться с другими пользователями канала.
''', parse_mode='html')




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
            Отправь мне свою историю и я отправлю её в канал)\n\n---------------------------------------
<b>! WARNING !</b>\n
1. Рекомендуется подумать и прислать мне текст, так как после отправки <b>он не может быть изменен</b>.\n
2. <b>ЗАПРЕЩАЕТСЯ</b> отправлять текст с вложениями! Пожалуйста, присылай только текстовые сообщения без прикрепленных файлов или медиафайлов.
            ''', parse_mode='html')
            bot.register_next_step_handler(message, process_post)


def process_post(message: types.Message):
    user_id = message.from_user.id
    story_text = message.text


    if story_text is not None:
        if check_advertising_text(story_text) is False:

            if not "/" in story_text:
            
                save_story(user_id, story_text)  # Сохраняем историю в базе данных
                publish_stories()
            else: # Если сообщение содержит символ "/", отправляем уведомление о запрете команд
                bot.send_message(message.from_user.id, "Извини, но нельзя отправлять команды/ссылки(\n\nПовтори вызов команды и снова отправь свою историю")
                bot.send_message(id_chat_info, f"#sent_a_link_or_a_command\n{story_text}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>",parse_mode='html')
        else: 
            bot.send_video(message.from_user.id, video='BAACAgIAAxkBAAICNWR6SK5IK8te9q4qFTVa5DWC5flTAALqMgACZr7ZS98yLje7RuTwLwQ', caption=f'Ну вот ты и попался, {user_first_name + last_name}\n\nНезя так')
            bot.send_message(id_chat_info, f"#block_words\n{story_text}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>",parse_mode='html')
            
    else:
        bot.send_message(message.from_user.id, 'Ай-ай-ай, кто-то не читает привила(\n\nНезя присылать вложения!')
    
        
        if message.content_type != 'text':
            if message.content_type == 'photo':
                if message.caption is not None:
                    if len(message.caption)>=1024: 
                        message.caption=message.caption[:-100]
                    else: message.caption=message.caption
                    bot.send_photo(id_chat_info, message.photo[0].file_id, caption=f"#sent_an_attachment\n{message.caption}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                else: bot.send_photo(id_chat_info, message.photo[0].file_id, caption=f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')

            elif message.content_type == 'video':
                if message.caption is not None:
                    if len(message.caption)>=1024: 
                        message.caption=message.caption[:-100]
                    else: message.caption=message.caption
                    bot.send_video(id_chat_info, message.video.file_id, caption=f"#sent_an_attachment\n{message.caption}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                else: bot.send_video(id_chat_info, message.video.file_id, caption=f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
            
            elif message.content_type == 'audio':
                if message.caption is not None:
                    if len(message.caption)>=1024: 
                        message.caption=message.caption[:-100]
                    else: message.caption=message.caption
                    bot.send_video(id_chat_info, message.audio.file_id, caption=f"#sent_an_attachment\n{message.caption}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                else: bot.send_video(id_chat_info, message.audio.file_id, caption=f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
            
            elif message.content_type == 'poll':

                bot.send_message(id_chat_info, f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                bot.send_poll(id_chat_info, question=message.poll.question, options=message.poll.options)
            
            elif message.content_type == 'location':
                bot.send_message(id_chat_info, f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                bot.send_location(id_chat_info, latitude=message.location.latitude, longitude=message.location.longitude)
            
            else:
                bot.send_message(id_chat_info, f"#sent_an_attachment\n Неизвестный тип вложения\n\<code>{message}</code>\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
        

def publish_stories():
    stories = get_stories()  # Получаем все истории из базы данных


    for story in stories:
        print(story.sent)
        if not story.sent:
            bot.send_message(id_channel, story.story_text)
            bot.send_message(story.user_id, "Твоя история отправлена на публикацию")
            story.sent = True
            delete_story(story.user_id, story.story_text)  # Удалить историю по её ID, а не по user_id и story_text

            break  # Прервать цикл после удаления истории



admin_input = {}  # Переменная для хранения ввода администратора

@bot.message_handler(commands=["send_all"])
def send_all(message: types.Message):
    if message.chat.type == 'private':
        user_first_name = str(message.chat.first_name) 
        last_name = str(message.chat.last_name)
        if last_name == 'None':
                last_name = ''
        if user_first_name == 'None':
            user_first_name = 'No Name'
        if str(message.from_user.id) == str(id_acc):
            bot.send_message(message.chat.id, "Введите текст для рассылки:")
            bot.register_next_step_handler(message, process_admin_input)
        else:
            bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды😡")
            bot.send_message(id_chat_info, f"#ввел_send_all\n\n{user_first_name} - {last_name} -- <code>{message.from_user.id}</code>",parse_mode='html')

        def process_admin_input(message: types.Message):
            user_input = message.text
            send_newsletter(user_input)

        def send_newsletter(text_to_send):
            # Отправка сообщений пользователям
            for user_id in get_user():
                try:
                    bot.send_photo(user_id, photo='AgACAgIAAxkBAAICqmR66pLDbMNcdmNL3kxY4_oOCfjVAAJAyTEbZr7ZS2blodlh4nZLAQADAgADeAADLwQ', caption=text_to_send)
                except Exception as e:
                    update_user_active_status(user_id, False)
                    print(f"Ошибка при отправке новостей пользователю {user_id}: {str(e)}")
                    bot.send_message(id_chat_info, f"#blocked_bot\n\n<code>{user_id}</code>",parse_mode='html')

            bot.send_message(id_acc, "Рассылка выполнена успешно!")







if __name__ == '__main__':
    # publish_stories()  # Выполняем функцию publish_stories в одном потоке
    bot.polling(none_stop=True)
