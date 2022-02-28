import os
import json
import random

from aiogram import Bot, Dispatcher, types, executor


bot = Bot(os.environ.get('RANDOM_DECKS_KEY'))
dp = Dispatcher(bot)

def add_data(string_to_add: str, target_file: str):
    try:
        with open(target_file, 'r') as target_info:
            players = json.load(target_info)
        players.append(string_to_add)
        with open(target_file, 'w') as target_info:
            json.dump(players, target_info)
    except Exception:
        with open(target_file, 'w') as target_info:
            json.dump([string_to_add], target_info)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, text='Для добавления данных "/pl имя игрока" или "/dk название колоды"; Для выдачи колод игрокам используй /decks; Для очистки используй /clean')

@dp.message_handler(commands=['pl'])
async def add_player(message: types.Message):
    parsed_message = message.text.split(' ', 1)
    add_data(parsed_message[1], 'random-players.json')
    await bot.send_message(message.chat.id, f'Добавлен игрок {parsed_message[1]}')

@dp.message_handler(commands=['dk'])
async def add_deck(message: types.Message):
    parsed_message = message.text.split(' ', 1)
    add_data(parsed_message[1], 'random-decks.json')
    await bot.send_message(message.chat.id, f'Добавлена колода {parsed_message[1]}')

@dp.message_handler(commands=['decks'])
async def generate_data(message: types.Message):
    with open('random-players.json', 'r') as target_info:
        players = json.load(target_info)

    with open('random-decks.json', 'r') as target_info:
        decks = json.load(target_info)

    if len(decks) < len(players):
        await bot.send_message(message.chat.id, f'Получается {decks} колод на {players} игроков.')
    
    for _ in range(10):
        random.shuffle(players)
        random.shuffle(decks)
    
    target_output_data = dict(zip(players, decks))
    target_output = ''
    for player, deck in target_output_data.items():
        target_output += f'{player} - {deck};\n'
    
    await bot.send_message(message.chat.id, target_output)

@dp.message_handler(commands=['clean'])
async def clean_data(message: types.Message):
    os.remove('random-decks.json')
    os.remove('random-players.json')
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
