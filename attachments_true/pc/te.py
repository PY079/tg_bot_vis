import telebot, time, os, chardet, logging, sys
from telebot import types
from data import t_token_tg_b, t_id_att, t_id_channel, id_chat_info, t_blyat, id_acc, t_warning
from attach import create_tables, check_user, save_media_entry, delete_media_entries
from blacklist import check_user_existence, ban_user, unban_user
from database import save_story, get_stories, delete_story
from adv_check import check_advertising_text
from send_message_datab import add_user, update_user_active_status, get_user

sys.stdout.reconfigure(encoding='utf-8')


os.system('cls')
print('\n\nБОТ ЗАПУЩЕН\n\n')

bot = telebot.TeleBot(t_token_tg_b)

logging.basicConfig(level=logging.DEBUG)
@bot.message_handler(commands=['start'], func=lambda message: not check_user_existence(message.from_user.id))
def start(m: types.Message):
    if m.chat.type == 'private':
        user_id = m.from_user.id
        user_first_name = str(m.from_user.first_name)
        last_name = str(m.from_user.last_name)
        # Проверка имени пользователя на наличие только букв и цифр

        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'No Name'

        if add_user(user_id) is not False:
            bot.send_message(id_chat_info,f'#new_user\n{last_name} {user_first_name}\n<code>{user_id}</code>',parse_mode='html')


        bot.send_message(m.from_user.id, text=f'''


Привееет, <b>{user_first_name} {last_name}</b>, делись с нами своими историями
А другие тебя поддержат!
Будь добрее)\n\n
В данный момент бот написан на 100%.
Работает круглосуточно\n
Если <b>возникают ошибки</b>, то пишите <a href='t.me//JKPyGtH'>сюда</a>\n
Бот создан разработчиком: <a href ='t.me//JKPyGtH'>PY079</a>
''', parse_mode='html', disable_web_page_preview=True)

@bot.message_handler(commands=['menu'], func=lambda message: not check_user_existence(message.from_user.id))
def menu(m: types.Message):
    if m.chat.type == 'private':
        user_id = m.from_user.id
        bot.send_message(m.chat.id, text='''
<b>Меню:</b>
1. /start - Команда, которую можно использовать для начала общения с ботом. Она инициирует диалог с ботом и позволяет выполнить определенные действия.\n
2. /menu - Команда, которая выводит это меню. При ее выполнении бот отправит тебе список доступных команд.\n
3. /suggest_a_post -  Команда, которую можно использовать для отправки своей истории боту с целью ее публикации. Ты можешь поделиться своими переживаниями, историями успеха или любыми другими историями, которые хотели бы поделиться с другими пользователями канала.\n
4. /attach_a_message позволяет отправить историю или сообщение с вложением. В первый раз отправь одно вложение с текстом (или без). После этого можно добавить еще вложения без текста до максимума в 10 штук.
Обрати внимание, что текст, который ты если напишешь в каждое вложение, то он будет прикреплен ко всем вложениям, а не как подпись к сообщению.
Когда закончишь добавлять вложения, нажми кнопку "Отправить".\n

Работает круглосуточно

''', parse_mode='html')




@bot.message_handler(commands=["suggest_a_post"], func=lambda message: not check_user_existence(message.from_user.id), content_types=['text'])
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
        if message.content_type != 'text':
            # Если получено сообщение с вложением, отправляем уведомление
            bot.send_message(message.from_user.id, "Извини, но нельзя отправлять сообщения с вложениями(")
        else:
            bot.send_message(message.from_user.id, '''
            Отправь мне свою историю и я отправлю её в канал)\n\n---------------------------------------
<b>! WARNING !</b>\n
Работает круглосуточно\n
1. Рекомендуется подумать и прислать мне текст, так как после отправки <b>он не может быть изменен</b>.\n
2. <b>ЗАПРЕЩАЕТСЯ</b> отправлять текст с вложениями! Пожалуйста, присылай только текстовые сообщения без прикрепленных файлов или медиафайлов.

            ''', parse_mode='html')
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
    

    if story_text is not None:
        if len(story_text)>=5:   
            wor = check_advertising_text(story_text)
            if wor is None:
                print(story_text)
                if not ('//' in story_text or '/start'in story_text or '/menu'in story_text or '/suggest_a_post'in story_text or '/attach_a_message'in story_text):
                                        
                    print(story_text)
                    save_story(user_id, story_text.replace('<','[').replace('>',']'))  # Сохраняем историю в базе данных
                    publish_stories(user_first_name, last_name)
                
                else: # Если сообщение содержит символ "/", отправляем уведомление о запрете команд
                    bot.send_message(message.from_user.id, "Извини, но нельзя отправлять команды/ссылки(\n\nПовтори вызов команды и снова отправь свою историю")
                    
                    log_text=f"#sent_a_link_or_a_command\n{story_text.replace('<','[').replace('>',']')}\n\n<code>{user_first_name} {last_name}</code> -- <code>{user_id}</code>"
                    if len(log_text) > 4096:
                        diff = len(log_text) - 4096
                        log_text=f"#sent_a_link_or_a_command\n{story_text.replace('<','[').replace('>',']')[:-diff]}\n\n<code>{user_first_name} {last_name}</code> -- <code>{user_id}</code>"
                    bot.send_message(id_chat_info, log_text, parse_mode='html')
                
                
            else:
                bot.send_video(message.from_user.id, video=t_blyat, caption=f'Ну вот ты и попался, {user_first_name} {last_name}\n\nНезя так')
                log_text1=f"#block_words\n{user_id} -- {user_first_name} {last_name}\n{wor}\n\n{story_text.replace('<','[').replace('>',']')}"
                ca=f"#block_words\n<code>{user_id}</code> -- <code>{user_first_name} {last_name}</code>\n{wor}\n\n{story_text.replace('<','[').replace('>',']')}"
                if len(log_text1) > 4096:
                    diff = len(log_text1) - 4096
                    ca=f"#block_words\n<code>{user_id}</code> -- <code>{user_first_name} {last_name}</code>\n{wor}\n\n{story_text.replace('<','[').replace('>',']')[:-diff]}"
                bot.send_message(id_chat_info, ca, parse_mode='html')

     
        else:
            bot.send_message(id_chat_info, f"#sent_few_characters\n\n{story_text}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
    else:
        bot.send_message(message.from_user.id, 'Ай-ай-ай, кто-то не читает правила(\n\nНезя присылать вложения!')

        if message.content_type != 'text':
            if message.content_type == 'photo':
                if message.caption is not None:

                    log_text1 = f"#sent_an_attachment\n{message.caption}\n\n{user_first_name} {last_name} -- {user_id}"
                    ca = f"#sent_an_attachment\n{message.caption.replace('<','[').replace('>',']')}\n\n<code>{user_first_name} {last_name}</code> -- <code>{user_id}</code>"
                    if len(log_text1) > 1024:
                        diff = len(log_text1) - 1024
                        ca = f"#sent_an_attachment\n{message.caption.replace('<','[').replace('>',']')[:-diff]}\n\n<code>{user_first_name} {last_name}</code> -- <code>{user_id}</code>"
                    bot.send_photo(id_chat_info, message.photo[0].file_id, caption=ca, parse_mode='html')

                else: bot.send_photo(id_chat_info, message.photo[0].file_id, caption=f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')

            elif message.content_type == 'video':
                if message.caption is not None:
                    

                    log_text1 = f"#sent_an_attachment\n{message.caption}\n\n{user_first_name} {last_name} -- {user_id}"
                    ca = f"#sent_an_attachment\n{message.caption.replace('<','[').replace('>',']')}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>"
                    if len(log_text1) > 1024:
                        diff = len(log_text1) - 1024
                        ca = f"#sent_an_attachment\n{message.caption.replace('<','[').replace('>',']')[:-diff]}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>"

                    bot.send_video(id_chat_info, message.video.file_id, caption=ca, parse_mode='html')
                else: bot.send_video(id_chat_info, message.video.file_id, caption=f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')

            elif message.content_type == 'audio':
                if message.caption is not None:
                
                    log_text1= f"#sent_an_attachment\n{message.caption}\n\n{user_first_name} {last_name} -- {user_id}"
                    ca = f"#sent_an_attachment\n{message.caption.replace('<','[').replace('>',']')}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>"
                    if len(log_text1) > 1024:
                        diff = len(log_text1) - 1024
                        ca = f"#sent_an_attachment\n{message.caption.replace('<','[').replace('>',']')[:-diff]}\n\n{user_first_name} {last_name} -- <code>{user_id}</code>"

                    bot.send_audio(id_chat_info, message.audio.file_id, caption=ca, parse_mode='html')

                else: bot.send_audio(id_chat_info, message.audio.file_id, caption=f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')

            elif message.content_type == 'poll':

                bot.send_message(id_chat_info, f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                bot.send_poll(id_chat_info, question=message.poll.question, options=message.poll.options)

            elif message.content_type == 'location':
                bot.send_message(id_chat_info, f"#sent_an_attachment\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                bot.send_location(id_chat_info, latitude=message.location.latitude, longitude=message.location.longitude)

            else:
                bot.send_message(id_chat_info, f"#sent_an_attachment\n Неизвестный тип вложения\n<code>{message}</code>\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')

        

def publish_stories(fi, la):
    stories = get_stories()  # Получаем все истории из базы данных


    for story in stories:
        print(story.sent)
        if not story.sent:
            bot.send_message(t_id_channel, story.story_text)
            
            bot.send_message(story.user_id, "Твоя история отправлена на публикацию")
            
            if len(story.story_text)>len(f'#text_in_post\n\n{fi} {la}\n{story.user_id}\n\n{story.story_text}'):
                symbols1 = len(f'#text_in_post\n\n{fi} {la}\n{story.user_id}\n\n{story.story_text}') - len(story.story_text)
                ca = f'#text_in_post\n\n<code>{fi} {la}</code> <code>{story.user_id}</code>\n\n{story.story_text[:-symbols1]}'
            else: 
                ca = f'#text_in_post\n\n<code>{fi} {la}</code> <code>{story.user_id}</code>\n\n{story.story_text}'
            bot.send_message(id_chat_info, ca,parse_mode='html')
            
            
            
            story.sent = True
            delete_story(story.user_id, story.story_text)  # Удалить историю по её ID, а не по user_id и story_text

            break  # Прервать цикл после удаления истории

can_add_media = {}
cou = {}  # Словарь для хранения списков file_id пользователей
log_t={}
@bot.message_handler(commands=['attach_a_message'], func=lambda message: not check_user_existence(message.from_user.id))
def handle_media_group(message: types.Message):
    user_id = message.from_user.id

    if user_id not in cou:
        cou[user_id] = []
        
    if user_id not in log_t:
        log_t[user_id] = []

    if user_id not in can_add_media:
        can_add_media[user_id]=True
    
    print('start',can_add_media)
    if can_add_media[user_id] ==False:
        can_add_media[user_id] = True
    print('upd start',can_add_media)
    if len(cou[user_id]) == 0:
        bot.send_message(user_id, '''В первый раз отправь мне одно вложение с текстом (или без). Остальные разы, если хочешь вложить больше, просто отправь вложение без текста (max 10).\n
Иначе текст, который ты написал, будет прикрепляться к каждому вложению, а не как подпись. ''')
    else:
        bot.send_message(user_id, 'Отправь мне вложение (всего можно вложить 10).')

    check_user(user_id, message)
    bot.register_next_step_handler(message, at_p)
    

def at_p(message: types.Message):
    log_text=[]
    user_id = message.from_user.id
    attach_text = message.caption
    user_first_name = str(bot.get_chat(user_id).first_name)
    last_name = str(bot.get_chat(user_id).last_name)
    # Проверка имени пользователя на наличие только букв и цифр

    if last_name == 'None':
        last_name = ''
    if user_first_name == 'None':
        user_first_name = 'No Name'
    
    if attach_text == None: attach_text=''
    else: 
        
        log_text=f'#attach\n\n{user_id}\n{last_name} {user_first_name}\n\n{attach_text}'
        if len(log_text) > 1024:
            diff = len(log_text) - 1024
            log_text=f'#attach\n\n{user_id}\n{last_name} {user_first_name}\n\n{attach_text[:-diff]}'

    if len(attach_text)>5 or len(attach_text)==0:
    
        wor = check_advertising_text(attach_text)
        if wor is None:
            if can_add_media[user_id] == True:    
                if not ('/' or 'start' or 'menu' or 'suggest_a_post' or 'attach_a_message' or '//') in attach_text:
                    
                    if message.content_type == 'video':
                        file_id = message.video.file_id
                        media = types.InputMediaVideo(file_id, caption=attach_text)
                        media1 = types.InputMediaVideo(file_id, caption=log_text)
                        cou[user_id].append(media)
                        log_t[user_id].append(media1)
                        save_media_entry(user_id, file_id, attach_text)

                    elif message.content_type == 'photo':
                        file_id = message.photo[0].file_id
                        media = types.InputMediaPhoto(file_id, caption=attach_text)
                        media1 = types.InputMediaPhoto(file_id, caption=log_text)
                        cou[user_id].append(media)
                        log_t[user_id].append(media1)
                        save_media_entry(user_id, file_id, attach_text)

                    elif message.content_type =='audio':
                        file_id=message.audio.file_id
                        media = types.InputMediaAudio(file_id, caption=attach_text)
                        media1 = types.InputMediaAudio(file_id, caption=log_text)
                        cou[user_id].append(media1)
                        log_t[user_id].append(media)
                    
                    elif message.content_type == 'document':
                        file_id=message.document.file_id
                        media = types.InputMediaDocument(file_id, caption=attach_text)
                        media1 = types.InputMediaDocument(file_id, caption=log_text)
                        cou[user_id].append(media)
                        log_t[user_id].append(media1)

                    else:
                        
                        if message.content_type =='poll':
                            bot.send_message(message.from_user.id,'Пока такое незя отправлять')
                            bot.send_message(id_chat_info, f"#sent_an_poll\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                            bot.send_poll(id_chat_info, question=message.poll.question, options=message.poll.options)
                        elif message.content_type == 'location':
                            bot.send_message(message.from_user.id,'Пока такое незя отправлять')
                            bot.send_message(id_chat_info, f"#sent_an_location\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                            bot.send_location(id_chat_info, latitude=message.location.latitude, longitude=message.location.longitude)
                        elif message.content_type =='text':
                                    
                            bot.send_message(id_chat_info, f"#sent_an_text\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')
                            bot.send_message(id_chat_info,message.text)
                            bot.send_message(message.from_user.id, 'В этой функции нельзя писать текст без вложений\n\nИспользуй тогда /suggest_a_post')

                        else:
                            bot.send_message(id_chat_info, f"#sent_an_none\n Неизвестный тип вложения\n<code>{message}</code>\n\n{user_first_name} {last_name} -- <code>{user_id}</code>", parse_mode='html')


                    if len(cou[user_id]) > 0 and len(cou[user_id])<=10:
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        send_button = types.InlineKeyboardButton('Отправить', callback_data='send_media')
                        add_button = types.InlineKeyboardButton('Добавить вложение', callback_data='add_media')
                        markup.add(send_button, add_button)
                        count_at =''
                        if len(cou[user_id]) ==1: count_at+='вложение'
                        elif len(cou[user_id])>=2 and len(cou[user_id]) <5: count_at+='вложения'
                        elif len(cou[user_id]) >5: count_at+='вложений'
                        bot.send_message(user_id, f'Если ты хочешь отправить {len(cou[user_id])} {count_at}, нажми кнопку "Отправить".', reply_markup=markup)

                    if len(cou[user_id])>10:
                        bot.send_message(message.from_user.id,'Больше 10 вложений нельзя!')
                    if len(cou[user_id])==9:
                        bot.send_message(message.from_user.id,'Осталось одно вложение!')

                else:
                    if len(attach_text) != 0: 
                        bot.send_message(message.from_user.id, "Извини, но нельзя отправлять команды/ссылки(\n\nПовтори вызов команды и снова отправь свою историю")
                        if len(attach_text) < len(f"#sent_a_link_or_a_command_at\n{attach_text}\n\n{user_first_name} {last_name} -- {user_id}"):
                            symbols=len(f"#sent_a_link_or_a_command_at\n{attach_text}\n\n{user_first_name} {last_name} -- {user_id}")-len(attach_text)
                            log_text=f'#sent_a_link_or_a_command_at\n{attach_text[:-symbols]}\n\n<code>{user_first_name} {last_name}</code> -- <code>{user_id}</code>'
                        else: 
                            log_text=f'#sent_a_link_or_a_command_at\n{attach_text}\n\n<code>{user_first_name} {last_name}</code> -- <code>{user_id}</code>'
                        bot.send_message(id_chat_info, log_text.replace('<','[').replace('>',']'), parse_mode='html')
            
            else: 
                bot.send_message(user_id,'Ты уже отправил историю\n\nВведи команду ещё раз и отправь историю с вложениями')
        else:
            bot.send_video(message.from_user.id, video=t_blyat, caption=f'Ну вот ты и попался, {user_first_name} {last_name}\n\nНезя так')
            if len(attach_text)<=len(f'#block_word_at\n\n{user_id} {last_name} {user_first_name}\n\n{attach_text}'):
                symbol=len(f'#block_word_at\n\n{user_id}\n{last_name} {user_first_name}\n\n{attach_text}')-len(attach_text)
                lor=f'#block_word_at\n\n{user_id}\n{last_name} {user_first_name}\n{wor}\n\n{attach_text[:-symbol]}'
            else:
                lor=f'#block_word_at\n\n{user_id}\n{last_name} {user_first_name}\n{wor}\n\n{attach_text}'
            bot.send_message(id_chat_info,lor)
        


@bot.callback_query_handler(func=lambda call: call.data == 'send_media')
def send_media_callback(call):
    user_id = call.from_user.id

    if user_id in cou and len(cou[user_id]) > 0:
        try:
            # print(cou[user_id])
            bot.send_media_group(t_id_att, media=cou[user_id])
            bot.send_media_group(id_chat_info, media=log_t[user_id])
            cou[user_id].clear()
            log_t[user_id].clear()
            can_add_media[user_id]=False
        
            # Получаем список file_id для удаления
            file_ids = [media.file_id for media in cou[user_id]]


            bot.send_message(user_id, '''Твоя история будет рассмотрена.\n
Спасибо, что воспользовались нашим ботом!
Мы желаем вам удачного пользования и приятного полета.''')
        except telebot.apihelper.ApiException as e:
            error_code = e.result.status_code
            error_description = e.result.json()['description']
            if error_code == 400 and 'audio can\'t be mixed with other media types' in error_description:
            # Обработка ошибки, если аудио не может быть смешано с другими типами медиа
                bot.send_message(user_id, 'Ошибка: аудио не может быть смешано с другими типами медиа.\n\nСброс всех твоих отправленных вложений')
            elif error_code == 400 and 'document can\'t be mixed with other media types' in error_description:
                bot.send_message(user_id, 'Ошибка: документ не может быть смешан с другими типами медиа.\n\nСброс всех твоих отправленных вложений')
            else:
            # Обработка других возможных ошибок
                bot.send_message(user_id, f'{error_code}\n\nПроизошла ошибка: {error_description}\n\nСброс всех твоих отправленных вложений')
                bot.send_message(id_chat_info, f'{error_code}\n\nПроизошла ошибка: {error_description}\n\n{bot.get_chat(user_id).first_name} {bot.get_chat(user_id).last_name}')
        finally: 
            print('finaly',can_add_media)
            can_add_media[user_id] = False
            delete_media_entries()
            cou.clear()
            log_t.clear()
    else:
        bot.answer_callback_query(call.id, text='Нет вложений для отправки.')


@bot.callback_query_handler(func=lambda call: call.data == 'add_media')
def add_media_callback(call):
    user_id = call.from_user.id

    print(can_add_media)

    if user_id not in cou:
        print('add_media',can_add_media)
        cou[user_id] = []
        can_add_media[user_id] = False
        

    if can_add_media[user_id] == True:
        bot.send_message(user_id, 'Отправь мне вложение')
        bot.register_next_step_handler(call.message, at_p)
    else:
      bot.send_message(user_id,'Невозможно добавить вложения. \n\nИстория уже отправлена.')




admin_input = {}  # Переменная для хранения ввода администратора

@bot.message_handler(commands=["send_all"])
def send_all(message: types.Message):
    if message.chat.type == 'private':
        user_first_name = str(message.chat.first_name)
        last_name = str(message.chat.last_name)
        # Проверка имени пользователя на наличие только букв и цифр

        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'No Name'

        def process_admin_input(message: types.Message):
            user_input = message.text
            send_newsletter(user_input)

        if str(message.from_user.id) == str(id_acc):
            bot.send_message(message.chat.id, "Введите текст для рассылки:")
            bot.register_next_step_handler(message, process_admin_input)
        else:
            bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды😡")
            bot.send_message(id_chat_info, f"#ввел_send_all\n\n{user_first_name} - {last_name} -- <code>{message.from_user.id}</code>",parse_mode='html')


        def send_newsletter(text_to_send):
            # Отправка сообщений пользователям
            for user_id in get_user():
                try:
                    bot.send_photo(user_id, photo=t_warning, caption=text_to_send)
                    time.sleep(2)
                    update_user_active_status(user_id, True)
                    bot.send_message(id_chat_info,f"#successful_mailing\n\nУдачная отправка новостей пользователю {user_id}")
                except Exception as e:
                    update_user_active_status(user_id, False)
                    print(f"Ошибка при отправке новостей пользователю {user_id}: {str(e)}")
                    bot.send_message(id_chat_info, f"#blocked_bot\n\n<code>{user_id}</code>\n\n<code>{str(e)}</code>",parse_mode='html')

            bot.send_message(id_acc, "Рассылка выполнена успешно!")

@bot.message_handler(commands=["ban"])
def b_u(message: types.Message):
    if str(message.from_user.id) == str(id_acc):
        bot.send_message(id_acc, 'Отправь мне id пользователя, чтобы заблокировать')
        bot.register_next_step_handler(message, b_u2)

def b_u2(message: types.Message):
    if check_user_existence(message.text) == False:
        ban_user(message.text)


        user_first_name = str(bot.get_chat(message.text).first_name)
        last_name = str(bot.get_chat(message.text).last_name)
        # Проверка имени пользователя на наличие только букв и цифр

        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'No Name'
        

        bot.send_message(id_acc, 'Пользователь заблокирован')
        bot.ban_chat_member(t_id_channel,message.text)
        bot.send_message(id_chat_info,f'<code>{message.text}</code>\n<code>{user_first_name}</code> <code>{last_name}</code> заблокирован', parse_mode='html')
    else:
        bot.send_message(id_acc, 'Пользователь уже заблокирован')

@bot.message_handler(commands=["un_ban"])
def ub_u(message: types.Message):
    if str(message.from_user.id) == str(id_acc):
        bot.send_message(id_acc, 'Отправь мне id пользователя, чтобы разблокировать')
        bot.register_next_step_handler(message, ub_u2)

def ub_u2(message: types.Message):
    if check_user_existence(message.text):
        unban_user(message.text)

        user_first_name = str(bot.get_chat(message.text).first_name)
        last_name = str(bot.get_chat(message.text).last_name)
        # Проверка имени пользователя на наличие только букв и цифр

        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'No Name'

        bot.unban_chat_member(t_id_channel,message.text)
        bot.send_message(id_acc, 'Пользователь разблокирован')
        bot.send_message(id_chat_info,f'<code>{message.text}</code>\n<code>{user_first_name}</code> <code>{last_name}</code> разблокирован', parse_mode='html')
    else:
        bot.send_message(id_acc, 'Пользователь уже разблокирован')



@bot.message_handler(commands=["send_ch"])
def send_ch(message: types.Message):
    print(type(message.from_user.id))
    print(type(id_acc))
    if message.chat.type == 'private':

        if str(message.from_user.id) == str(id_acc):


            bot.send_photo(t_id_channel,t_warning,'''
Бот залит на <b>хостинг</b> (чужой пк, который будет каждый день работать в другой стране)
Иногда бот будет вылетать. Как только я замечу это, то <b>запущу его и сделаю рассылку</b>.\n
[Все текста, которые не отправились, отправьте повторно]\n
Не бойтесь, рассылки будут только важные и не будет никакой рекламы

Рассылку имеет право использовать <b>только <a href ='t.me/JKPyGtH'>создатель этого бота</a></b>

[ ]- данное предложение будет всегда повторяться в рассылках''', parse_mode='html')

            for user_id in get_user():
                try:
                    bot.send_photo(user_id, photo=t_warning, caption='''
Бот залит на <b>хостинг</b> (чужой пк, который будет каждый день работать в другой стране)
Иногда бот будет вылетать. Как только я замечу это, то <b>запущу его и сделаю рассылку</b>.\n
[Все текста, которые не отправились, отправьте повторно]\n
Не бойтесь, рассылки будут только важные и не будет никакой рекламы

Рассылку имеет право использовать <b>только <a href ='t.me/JKPyGtH'>создатель этого бота</a></b>

[ ]- данное предложение будет всегда повторяться в рассылках''', parse_mode='html')
                except Exception as e:
                    update_user_active_status(user_id, False)
                    print(f"Ошибка при отправке новостей пользователю {user_id}: {str(e)}")
                    bot.send_message(id_chat_info, f"#blocked_bot\n\n<code>{user_id}</code>",parse_mode='html')
            bot.send_message(id_acc, "Рассылка выполнена успешно!")




def main():
    bot.polling()

if __name__ == "__main__":
    main()


