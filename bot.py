import os
import json
import random

from aiogram import Bot, Dispatcher, types, executor


bot = Bot(os.environ.get('RANDOM_DECKS_KEY'))
dp = Dispatcher(bot)

def add_data(data_to_add: list, target_file: str):
    try:
        with open(target_file, 'r') as target_info:
            players = json.load(target_info)
        players.extend(data_to_add)
        with open(target_file, 'w') as target_info:
            json.dump(players, target_info)
    except Exception:
        with open(target_file, 'w') as target_info:
            json.dump(data_to_add, target_info)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, text='Для добавления игроков и колод используй команду "/pl" и "/dk, после чего вводи имена игроков, например: /pl Игрок 1\nИгрок2 и т.д.\nДля выдачи колод используй команду /generate.\nДля просмотре списков используй команды /decks и /players.\nНе забудь прибраться с помощью команды /clean"')

@dp.message_handler(commands=['pl'])
async def add_player(message: types.Message):
    parsed_message = message.text.split(' ', 1)
    players = parsed_message[1].split('\n')
    add_data(players, 'random-players.json')
    await bot.send_message(message.chat.id, f'Список игроков обновлен')

@dp.message_handler(commands=['dk'])
async def add_deck(message: types.Message):
    parsed_message = message.text.split(' ', 1)
    decks = parsed_message[1].split('\n')
    add_data(decks, 'random-decks.json')
    await bot.send_message(message.chat.id, f'Список колод обновлен')

@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.chat.id, text='Для добавления игроков и колод используй команду "/pl" и "/dk, после чего вводи имена игроков, например: /pl Игрок 1\nИгрок2 и т.д.\nДля выдачи колод используй команду /generate.\nДля просмотре списков используй команды /decks и /players.\nНе забудь прибраться с помощью команды /clean"')

@dp.message_handler(commands=['players', 'decks'])
async def get_list(message: types.Message):
    errormsg = ''
    target_file = ''
    header = ''
    if message.text == '/players':
        errormsg = 'Сначала надо добавить игроков'
        target_file = 'random-players.json'
        header = 'Текущие игроки:\n'
    else:
        errormsg = 'Сначала надо добавить колоды'
        target_file = 'random-decks.json'
        header = 'Текущие колоды:\n'
    try:
        with open(target_file) as players_file:
            file_data = json.load(players_file)
            output_string = '\n'.join([i for i in file_data])
            await bot.send_message(message.chat.id, text=f'{header}{output_string}')
    except FileNotFoundError:
        await bot.send_message(message.chat.id, text=errormsg)

@dp.message_handler(commands=['generate'])
async def generate_data(message: types.Message):
    with open('random-players.json', 'r') as target_info:
        players = json.load(target_info)

    with open('random-decks.json', 'r') as target_info:
        decks = json.load(target_info)

    if len(decks) < len(players):
        await bot.send_message(message.chat.id, f'Получается {decks} колод на {players} игроков. Нельзя сгенерировать пары.')
    
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
    for target_file in ['random-decks.json', 'random-players.json']:
        try:
            os.remove(target_file)
        except Exception as e:
            continue
    bot.send_message(message.chat.id, 'Файлы удалены. Можно дать новый список.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
