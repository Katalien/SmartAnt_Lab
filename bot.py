import os
import sqlite3
import subprocess
from time import sleep
import logging
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

con = sqlite3.connect('results.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS results')
cur.execute('CREATE TABLE results (surname TEXT, name TEXT, group_num INTEGER, score INTEGER, ass INTEGER)')

bot = Bot(token="5951480835:AAGwvuqdswaiMoag81Qw1HMCsiJR9ssKm2E")
dp = Dispatcher(bot)

logging.basicConfig(filename='.log', encoding='utf-8', level=logging.INFO)


async def start(message: types.Message):
    await message.answer(
        "Hi! I'm your Lab Checker bot. Send me your Java project as a file and I'll compile and test it for you.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def process_java(message: types.Message):
    caption = message.from_user.id
    # surname, name, group = caption.split('-')
    surname, name, group = "A", "B", "2"
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    filename = message.document.file_name
    extension = filename.split('.')[-1]
    if extension != 'java' or filename.split('.')[0] != 'Optimizer':
        await bot.send_message(chat_id=message.from_user.id, text="Не тот файл. Нужен файл Optimizer.java")
        return

    file = await message.document.download()
    print(file)
    file1 = open(file.name, 'r')
    file2 = open('src/main/java/com/play/Optimizer.java', 'w')
    file2.write(file1.read())
    file1.close()
    file2.close()
    run_test = ['mvn', 'clean', 'test']
    p_jar = subprocess.Popen(run_test)
    p_jar.wait()
    if os.path.isfile('target/results.out'):
        with open("target/results.out", "r") as score_file:
            score_file_text = score_file.read()
        if score_file_text == '':
            await message.answer("Time limit exceeded. Please optimize your code and try again.")
            return
        else:
            res = int(score_file_text)
            logging.info(f'run {surname}:{name} project - {res} points')
            ass = res  # TODO: assessment formula
            ans = cur.execute(f'SELECT * FROM results WHERE surname = ? AND name = ? AND group_num = ?',
                              (surname, name, group)).fetchall()
            if not ans:
                cur.execute(f'INSERT INTO results VALUES(?, ?, ?, ?, ?)', (surname, name, group, res, ass))
            else:
                cur.execute(f'UPDATE results SET score = ?, ass = ? WHERE surname = ? AND name = ? AND group_num = ?',
                            (res, ass, surname, name, group))
            con.commit()
            await message.answer(f'Great! Your program compiled and ran successfully. You scored {res} points.')


async def unknown(message: types.Message):
    await message.answer("Sorry, I didn't understand that command.")


dp.register_message_handler(start, commands=['start'])
# dp.register_message_handler(process_java, content_types=['document'])
dp.register_message_handler(unknown, commands=['help', 'info'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)