import telebot
bot = telebot.TeleBot('6456465134:AAEY-e_AeNibZIkPfSckR7lis_6U0UGej3k')
import random
from telebot import types
import copy

level = 0
secret_number = 0
random_massiv = [i for i in range(10)]

def check(s1, s2):
    ox = 0
    cow = 0
    i = 0
    while i < len(s1):
        if s1[i] == s2[i]:
            ox += 1
            s1 = s1[:i] + s1[i+1:]
            s2 = s2[:i] + s2[i+1:]
            continue
        i += 1
    i = 0
    while i < len(s1):
        if s1[i] in s2:
            cow += 1
            ind = s2.index(s1[i])
            s1 = s1[:i]+s1[i+1:]
            s2 = s2[:ind]+s2[ind+1:]
            continue
        i+=1
    return ox, cow
         
@bot.message_handler(commands=['start'])
def startBot(message):
    start_message = "Привет, я бот, который сыграет с тобой в игру Быки и Коровы\n"
    start_message += "Если хочешь узнать правила введи /help\n"
    start_message += "Выбери уровень(чтобы узнать описание уровней введи /info):\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, 14):
        markup.add(types.KeyboardButton(str(i)))
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['help'])
def helper(message):
    help_message = "Задача игрока – отгадать число, загаданное мной. В свой ход игрок называет число. Я сравниваю названное число с тем, что я загадал, и отвечаю, сколько цифр угадано и стоит на нужном месте, это «быки», а сколько цифр угадано, но стоит не на своём месте. Это – «коровы».\n"
    help_message += "Выбери уровень(чтобы узнать описание уровней введи /info):\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, 14):
        markup.add(types.KeyboardButton(str(i)))
    bot.send_message(message.chat.id, help_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=["info"])
def information(message):
    info_message = "1 - 4-ёх значное число без повторений\n"
    info_message += "2 - 5-ти значное число без повторений\n"
    info_message += "3 - 6-ти значное число без повторений\n"
    info_message += "4 - 7-ми значное число без повторений\n"
    info_message += "5 - 8-ми значное число без повторений\n"
    info_message += "6 - 9-ти значное число без повторений\n"
    info_message += "7 - 10-ти значное число без повторений\n"
    info_message += "8 - 4-ёх значное число с возможными повторениями\n"
    info_message += "9 - 5-ти значное число с возможными повторениями\n"
    info_message += "10 - 6-ти значное число с возможными повторениями\n"
    info_message += "11 - 7-ми значное число с возможными повторениями\n"
    info_message += "12 - 8-ми значное число с возможными повторениями\n"
    info_message += "13 - 9-ти значное число с возможными повторениями\n"
    info_message += "14 - 10-ти значное число с возможными повторениями\n"
    info_message += "Выбери уровень:\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, 15):
        markup.add(types.KeyboardButton(str(i)))
    bot.send_message(message.chat.id, info_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def play(message):
    global secret_number
    global level
    global random_massiv
    try:
        if level == 0 and (int(message.text) > 0 and int(message.text) < 15):
            level = int(message.text)
            if level < 8:
                buff_massiv = copy.deepcopy(random_massiv)
                for i in range(level + 3):
                    ind = random.randint(0, len(buff_massiv) - 1)
                    if i == 0 and ind == 0: ind = 1
                    secret_number += buff_massiv[ind]*(10**(level+2-i))
                    buff_massiv.pop(ind)
            else:
                buff_massiv = copy.deepcopy(random_massiv)
                for i in range(level - 4):
                    ind = random.randint(0, len(buff_massiv) - 1)
                    if i == 0 and ind == 0: ind = 1
                    secret_number += buff_massiv[ind]*(10**(level-5-i))
            answer_message = "Я загадал число, введи своё предположение:"
        elif len(message.text) <= 10 and int(message.text):
            variant = int(message.text)
            s_secret_number = str(secret_number)
            if len(message.text) == len(s_secret_number):
                ox, cow = check(message.text, s_secret_number)
                if ox == len(s_secret_number):
                    level = 0
                    secret_number = 0
                    answer_message = "Вы победили!!! Поздравляю!!\n"
                    answer_message += "\U0001F386\n"
                    answer_message += "Для новой игры введите /start\n"
                    video = open("video.mp4", "rb")
                    bot.send_video(message.chat.id, video)
                    video.close()
                else:
                    answer_message = f"У вас {ox} быков и {cow} коров))\n"
                    answer_message += "Быков - " + "\U0001F403"*ox + "\n"
                    answer_message += "Коров - " + "\U0001F404"*cow + "\n"
            else:
                answer_message = "Вы ввели неправильно значное число, повторите ввод\n"
        else:
            answer_message = "Я не понял, что вы ввели, введите число нужной длины\n"
        bot.send_message(message.chat.id, answer_message, parse_mode='html')
    except Exception:
        answer_message = "Я не понял что Вы ввели, введите число"
        bot.send_message(message.chat.id, answer_message, parse_mode='html')


bot.infinity_polling()