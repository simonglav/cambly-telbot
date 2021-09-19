from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from parser import Parser
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hi!\nSend me a word you want to know about!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Send me an english word and I'll respond you with a description of that word.")


@dp.message_handler()
async def echo_message(msg: types.Message):
    description_dict = Parser(msg.text).get_description()
    if description_dict:
        if 'name' in description_dict and 'definition' in description_dict:
            def_message = description_dict['name'] + ' - ' + description_dict['definition']
            await bot.send_message(msg.from_user.id, def_message)
    else:
        await bot.send_message(msg.from_user.id, 'There is no such word in the dictionary!')


if __name__ == '__main__':
    print("Bot is currently running...\nTo stop press Ctrl+C")
    executor.start_polling(dp)
