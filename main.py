import random
import telebot
from database import Database
from messages import MESSAGES as ms
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

bot = telebot.TeleBot('5447229707:AAHAZit8GX0K6HvQWkBi__CiNQzf5qxI4g0')
db = Database('database.db')
white = []

@bot.message_handler(commands=['start', 'test'])
def command_answer(message):
  user_id = message.from_user.id
  if db.user_exist(user_id):
    pass
  else:
    db.add_user(user_id)
  uc = message.text[1:]
  if uc == 'start':
    db.edit_user(user_id, step='main')
    kb = start_kb(user_id)
    bot.send_message(user_id, ms['start'], parse_mode='markdownv2', reply_markup=kb)
  elif uc == 'test':
    kb = create_crosszero_board(user_id)
    bot.send_message(user_id, 'test', reply_markup=kb)

@bot.message_handler(content_types=['text'])
def text_answer(message):
  user_id = message.from_user.id
  um = message.text
  user_info = db.user_info(user_id)
  user_balance = user_info[1]
  user_step = user_info[2]
  if user_id in white:
    pass

  if um == '🖥 Личный кабинет':
    db.edit_user(user_id, step='lk')
    kb = InlineKeyboardMarkup()
    answer = ms['lk'].format(user_balance, user_id, random.randint(100, 150))
    bot.send_photo(user_id, open('img/sweexy.png', 'rb'), caption=answer, parse_mode='html', reply_markup=kb)
  elif um == '🎮 Игры':
    db.edit_user(user_id, step='all_games')
    bot.send_message(user_id, 'Вот список моих игр:', reply_markup=game_board())

  if user_step == 'all_games':
    if um == 'Крестики Нолики':
      db.edit_user(user_id, step='choice_opponent_type')
      kb = ReplyKeyboardMarkup()
      kb.add(InlineKeyboardButton('С другом'), InlineKeyboardButton('С ботом'))
      bot.send_message(user_id, 'Выбери, против кого будешь играть', reply_markup=kb)

  elif user_step == 'choice_opponent_type':
    if um == 'С другом':
      db.edit_user(user_id, step='get_opponent_id')
      bot.send_message(user_id, 'Введи ID друга:')
    elif um == 'С ботом':
      bot.send_message(user_id, 'Данная функция в разработке...')

  elif user_step == 'get_opponent_id':
    if isInt(um):
      if db.user_exist(um):
        if db.user_info(um)[6] != 'in_game':
          db.edit_user(user_id, step='send_game-request', opponent=um)
          bot.send_message(user_id, 'Заявка отправлена пользователю!')
          kb = InlineKeyboardMarkup()
          kb.add(InlineKeyboardButton('Принять ✅', callback_data=f'game-request_{user_id}_yep'), InlineKeyboardButton('Отклонить ❌', callback_data=f'game-request_{user_id}_nope'))
        else:
          bot.send_message(user_id, 'Пользователь находится в игре!')
      else:
        bot.send_message(user_id, 'Пользователь не найден')
    else:
      bot.send_message(user_id, 'Нужно ввести ID пользователя!')


@bot.callback_query_handler(func=lambda call:True)
def call_answer(call):
  user_id = call.from_user.id
  user_info = db.user_info(user_id)
  user_balance = user_info[1]
  user_step = user_info[2]

  if call.data[:12] == 'game-request':
    opponent_id = call.data.split('_')[1]
    if call.data.split('_')[2] == 'yep':
      db.edit_user(user_id, opponent=opponent_id, status='in_game', step='start_game', in_game='cross-zero')
      db.edit_user(opponent_id, status='in_game', step='start_game', in_game='cross-zero')
      game_step = random.choice([opponent_id, user_id])
      db.create_game_crosszero(opponent_id, user_id, game_step)
      game_message = ms['game'].format('cross-zero', game_step)
      bot.send_message(user_id, game_message, parse_mode='html')
    else:
      bot.send_message(opponent_id, 'Ваша заявка была отклонена!')

  if user_step == 'lk':
    if call.data == 'pay_up':
      summ = bot.send_message(user_id, '*Введите сумму пополнения\nМинимальная сумма \- 10₽*', parse_mode='markdownv2')
      bot.register_next_step_handler(summ, pay_up)


def pay_up(message):
  user_id = message.from_user.id
  summ = message.text
  if isInt(summ):
    summ = int(summ)
    if summ >= 10:
      pass
    else:
      bot.send_message(user_id, 'Минимальная сумма пополнения - 10')
  else:
    bot.send_message(user_id, 'Нужно ввести число!')


def isInt(num):
  try:
    num = int(num)
    return True
  except:
    return False


def start_kb(user_id):
  kb = ReplyKeyboardMarkup(resize_keyboard=True)
  kb.add(InlineKeyboardButton('🖥 Личный кабинет'), InlineKeyboardButton('🎮 Игры'))
  return kb

def game_board():
  kb = ReplyKeyboardMarkup()
  kb.add(InlineKeyboardButton('Крестики Нолики'))
  return kb

def create_crosszero_board(creator):
  game_info = db.cz_info(creator)
  blocks = []
  for i in range(3, 11):
    if game_info[i] == 0:
      blocks.append(InlineKeyboardButton('None', callback_data=f'block_{i}'))
    else:
      blocks.append(InlineKeyboardButton(i, callback_data=f'block_{i}'))
  # for i in range()
  kb = InlineKeyboardMarkup()
  return kb

bot.polling(none_stop=True)