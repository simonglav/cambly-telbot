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
async def process_response(msg: types.Message):
    description_dict = Parser(msg.text).get_description()
    if description_dict:
        if 'image' in description_dict:
            await bot.send_photo(msg.from_user.id, description_dict['image'])

        if 'name' in description_dict and 'definition' in description_dict:
            def_message = description_dict['name'].capitalize() + ' - ' + description_dict['definition']
            await bot.send_message(msg.from_user.id, def_message)

        if 'morphology' in description_dict:
            morph = description_dict['morphology']
            # There are only 'adjective', 'adverb' and 'interjection' start with vowel
            if morph[0] in ('a', 'i'):
                morph_message = "It's an " + morph
            else:
                morph_message = "It's a " + morph
            await bot.send_message(msg.from_user.id, morph_message)

        if 'pronunciations' in description_dict:
            pronoun = description_dict['pronunciations']
            if isinstance(pronoun, str):
                await bot.send_voice(msg.from_user.id, pronoun)
            else:
                await bot.send_voice(msg.from_user.id, pronoun['UK'])
                await bot.send_voice(msg.from_user.id, pronoun['US'])

        if 'examples' in description_dict:
            examples = description_dict['examples']
            if len(examples) == 1:
                examp_message = 'Example:\n1. ' + examples.pop()
            else:
                examp_message = 'Examples:\n1. ' + examples.pop() + '\n2. ' + examples.pop()
            await bot.send_message(msg.from_user.id, examp_message)



    else:
        await bot.send_message(msg.from_user.id, 'There is no such word in the dictionary!')


if __name__ == '__main__':
    print("Bot is currently running...\nTo stop press Ctrl+C")
    executor.start_polling(dp)
