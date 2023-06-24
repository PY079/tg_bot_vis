import os
def check_advertising_text(text):
    pk = r'C:\Users\User\Desktop\tg_bot_mus\post_tg\1\bot_forbidding_attachments\ads_text.txt'
    # home_dir = os.path.expanduser('~')
    # da = os.path.join(home_dir,'bots/tg_bot_vis/attachments_true/ads_text.txt')
    with open(pk,'r', encoding='utf-8') as f:
        advertising_words = f.read().splitlines()

        for word in advertising_words:
            if word in text.lower():
                return word  # Текст содержит рекламный контент

        return None  # Текст не содержит рекламный контент

# Пример использования




def append_unique_sentences(file_path, sentences, fi):
    existing_sentences = set()

    # Чтение существующих предложений из файла
    with open(file_path, 'r') as file:
        existing_sentences = set(file.read().splitlines())

    # Фильтрация предложений и запись уникальных в файл
    with open(fi, '+a') as file:
        for sentence in sentences:
            if sentence not in existing_sentences:
                file.write(sentence + '\n')
                existing_sentences.add(sentence)


# append_unique_sentences('C:/Users/User/Desktop/tg_bot_mus/post_tg/1/1.txt', [text])






# block_list=['тогда тебе','записывайтесь','ждём вас','ждем вас',
#             'ждём тебя','ждем тебя','перейди по ссылке', 'перейдите по ссылке',
#             'наш адрес', 'наши адреса', 'записывайся', 'записывайтесь',
#             'записывайся по номеру',
#             'переходите по ссылке', 'перейди по ссылке', 'предложение ограниченно',
#             'предложения ограничены', 'цены вырастут', 'цена вырастет',
#             'заходите в сообщество', 'заходи в общество', 'многое другое в паблике',
#             'многое другое в пабликах', 'самые низкие цены', 'самя низкая цена',
#             'низкие цены', 'низкая цена', 'переходи по ссылки в комментариях',
#             'переходите по ссылке в комментариях', 'переходите по ссылкам в комментариях',
#             'все подробности в пабликах', 'все подробности в паблике', 'подробная информация в группе',
#             'подробная информация в группах', 'качественно','недорого',
#             'качественно и не дорого', 'пишите и звоните',' подписывайся на канал',
#             'подпсывайтесь на канал', 'подписывайся','спешите обновить',
#             'спеши обновить', 'у нас вы найдете', 'у нас вы найдёте',
#             'у нас ты найдёшь','у нас ты найдешь','сделайте заказ', 'сделай заказ',
#             'сделайте заказ прямо сейчас','сделай заказ прямо сейчас', 'скидка',
#             'скидки','скидкам','скидок','низкие цены', 'низким ценам',
#             'по низким ценам','низкая цена','акция','акции','закажи','закажите']
# post_ads = any(ad in text for ad in block_list)