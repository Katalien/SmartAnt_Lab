import os
import sqlite3
import subprocess
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
#
bot = Bot(token="5951480835:AAH3MHJYNlovrilj3wvV6NllZg-pV-gycaI")
dp = Dispatcher(bot)

# logging.basicConfig(filename='.log', encoding='utf-8', level=logging.INFO)
con = sqlite3.connect('results.db')
cur = con.cursor()
# cur.execute('DROP TABLE results')
# cur.execute('CREATE TABLE results (name_group TEXT, score INTEGER, ass INTEGER)')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    meet_message = "Привет! Я буду проверять твой код во время лабораторной работы.\nОтправь мне файл Optimizer.java, добавь подпись в формате 'Фамилия Имя Группа' и жди результат.\n Желаю удачи! "
    await bot.send_message(chat_id=message.from_user.id, text=meet_message)

@dp.message_handler(content_types=types.ContentType.ANY)
async def process_java(message: types.Message):
    print("hui")
    if message.caption == None:
        await bot.send_message(chat_id=message.from_user.id, text="Укажи фимилию, имя и группу в подписи к файлу. Отправь файл заново с правильной подписью")
        return
    name_group = message.caption
    await bot.send_message(chat_id=message.from_user.id, text="Файл получил. Он в очереди на оценку, жди.")
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    filename = message.document.file_name
    extension = filename.split('.')[-1]
    if extension != 'java' or filename.split('.')[0] != 'Optimizer':
        await bot.send_message(chat_id=message.from_user.id, text="Не тот файл. Нужен файл Optimizer.java")
        return
    file = await message.document.download()
    file1 = open(file.name, 'r')
    file2 = open('src/main/java/com/play/Optimizer.java', 'w')
    file2.write(file1.read())
    file1.close()
    file2.close()
    run_test = ['mvn', 'clean', 'test']
    p_jar = subprocess.Popen(run_test, shell=True)
    p_jar.wait()
    # емли файл существует
    if os.path.isfile('result/hueta.csv'):
        # отк рыть и запомнить результат в переменную
        with open("result/hueta.csv", "r") as score_file:
            score_file_text = score_file.read()
        # если строка пустая, то сообщение пользователю
        if score_file_text == '':
            await message.answer("Упс...В твоем коде есть ошибка или он превышает время выполнения. Перепроверь и отправь заново.")
            return
        # если строка не пустая, то записать результат в таблицу
        else:
            res = int(score_file_text)
            ass = res  # TODO: assessment formula
            ans = cur.execute(f'SELECT * FROM results WHERE name_group = ?',
                              (name_group,)).fetchall()
            if not ans:
                cur.execute(f'INSERT INTO results VALUES(?, ?, ?)', (name_group, res, ass))
            else:
                cur.execute(f'UPDATE results SET score = ?, ass = ? WHERE name_group = ?',
                            (res, ass, name_group))
            con.commit()
            logging.info(f'run {name_group} project - {res} points')
            await message.answer(f'Молодец! Твоя программа прошла все тесты. Твой результат {res}.')
            return

async def unknown(message: types.Message):
    await message.answer("Прости, но я не знаю таких команд.")

#
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
