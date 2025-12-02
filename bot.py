# bot.py
import telebot

API_TOKEN = "8515664991:AAHVVZBWStgWPWeT1iXO97ewA0gGrc2cEsE"
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "Let's start! Please write your weight (kg):")
    bot.register_next_step_handler(message, get_weight)

def get_weight(message):
    chat_id = message.chat.id
    try:
        user_data[chat_id]['weight'] = float(message.text)
        bot.send_message(chat_id, "Write your height (cm):")
        bot.register_next_step_handler(message, get_height)
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid number for weight:")
        bot.register_next_step_handler(message, get_weight)

def get_height(message):
    chat_id = message.chat.id
    try:
        user_data[chat_id]['height'] = float(message.text)
        bot.send_message(chat_id, "Write your age:")
        bot.register_next_step_handler(message, get_age)
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid number for height:")
        bot.register_next_step_handler(message, get_height)

def get_age(message):
    chat_id = message.chat.id
    try:
        user_data[chat_id]['age'] = int(message.text)
        bot.send_message(chat_id, "Write your gender (male/female):")
        bot.register_next_step_handler(message, get_gender)
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid number for age:")
        bot.register_next_step_handler(message, get_age)

def get_gender(message):
    chat_id = message.chat.id
    gender = message.text.lower()
    if gender in ['male', 'm', 'ذكر', 'female', 'f', 'أنثى']:
        user_data[chat_id]['gender'] = gender
        bot.send_message(chat_id, "Write your activity multiplier:")
        bot.register_next_step_handler(message, get_activity)
    else:
        bot.send_message(chat_id, "Please enter 'male' or 'female':")
        bot.register_next_step_handler(message, get_gender)

def get_activity(message):
    chat_id = message.chat.id
    try:
        activity = float(message.text)
        if activity < 1 or activity > 2:
            raise ValueError
        user_data[chat_id]['activity'] = activity
        send_result(chat_id)
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid activity multiplier (1.2 to 1.9):")
        bot.register_next_step_handler(message, get_activity)

def send_result(chat_id):
    data = user_data[chat_id]
    weight = data['weight']
    height = data['height']
    age = data['age']
    gender = data['gender']
    activity = data['activity']

    if gender in ['male','m','ذكر']:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    tdee = bmr * activity

    reply = f"Estimated BMR: {int(bmr)} calories.\nEstimated TDEE: {int(tdee)} calories."
    bot.send_message(chat_id, reply)
    bot.send_message(chat_id, "Calculation done! You can start again with /start if you want.")

def run_bot():
    bot.infinity_polling()
