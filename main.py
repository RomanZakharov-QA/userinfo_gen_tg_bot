import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

TOKEN = 'your_token'
bot = TeleBot(TOKEN, parse_mode='html')
faker = Faker('ru_RU') 

main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_reply_markup.row(
    types.KeyboardButton(text="1️⃣"), types.KeyboardButton(text="2️⃣")
)
main_menu_reply_markup.row(
    types.KeyboardButton(text="5️⃣"), types.KeyboardButton(text="🔟")
)

@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭтот бот генерирует информацию для тестовых пользователей. "\
        "Выберите, сколько нужно пользователей",
        reply_markup=main_menu_reply_markup
    )

@bot.message_handler()
def message_handler(message: types.Message):
    payload_len = 0
    if message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя")
        return

    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Можете выбрать ещё раз",
        reply_markup=main_menu_reply_markup
    )
    
def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()