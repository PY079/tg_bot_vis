from data import token_tg_b, id_channel, id_chat_info
from send_message_datab import add_user
import telebot, os
print('')
os.system('cls')

bot = telebot.TeleBot(token_tg_b)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        add_user(user_id)
        user_first_name = str(message.chat.first_name)
        last_name = str(message.chat.last_name)
        if last_name == 'None':
            last_name = ''
        if user_first_name == 'None':
            user_first_name = 'Инкогнито'
        # Отправляем ответное сообщение пользователю
        bot.send_message(message.chat.id, f'''Привет, {user_first_name} {last_name}!\n
В данный момент бот <b>ОБНОВЛЯЕТСЯ</b>\n
Прошу тебя подождать и не писать ничего, пока обновление не завершится. Спасибо)\n
Ты будешь <b>уведомлен(a)</b>, когда обновление будет завершено.''',parse_mode='html')

        bot.send_message(id_chat_info,f'{user_first_name} {last_name} -- <code>{user_id}</code>\n\n{message.text}',parse_mode='html')

# Запускаем бота
bot.polling()
