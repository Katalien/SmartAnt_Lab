import os
import subprocess
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token="5951480835:AAGwvuqdswaiMoag81Qw1HMCsiJR9ssKm2E")
dp = Dispatcher(bot)

logging.basicConfig(filename='.log', encoding='utf-8', level=logging.INFO)


@dp.message_handler(content_types=types.ContentType.ANY)
async def process_java(message: types.Message):
    print("hui")
    if message.document:
        print("I an in procces_Java")
    surname, name, group = "A", "B", "2"
    await bot.send_message(chat_id=message.from_user.id, text="Файл получил. Он в очереди на оценку, жди.")
    print(surname, name, group)
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
            await message.answer("Time limit exceeded. Please optimize your code and try again.")
            return
        # если строка не пустая, то записать результат в таблицу
        else:
            res = int(score_file_text)
            logging.info(f'run {surname} project - {res} points')
            await message.answer(f'Great! Your program compiled and ran successfully. You scored {res} points.')
            return


async def unknown(message: types.Message):
    await message.answer("Sorry, I didn't understand that command.")


# dp.register_message_handler(start, commands=['start'])
# dp.register_message_handler(process_java, content_types=['document'])
# dp.register_message_handler(unknown, commands=['help', 'info'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
