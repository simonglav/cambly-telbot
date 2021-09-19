from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import WrongFileIdentifier

# Contains TOKEN = "{ your token }"
from config import TOKEN
from parser import Parser

# Standard messages
START_MESSAGE = "Hi!\nSend me a word you want to know about!"
HELP_MESSAGE = "Send me an english word and I'll respond you with a description of that word."
INVALID_INPUT_MESSAGE = 'There is no such word in the dictionary!'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(text=START_MESSAGE)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(text=HELP_MESSAGE)


@dp.message_handler()
async def process_response(msg: types.Message):
    description_dict = Parser(msg.text).get_description()

    if description_dict:
        if 'image' in description_dict:
            # Telegram API issues
            try:
                await bot.send_photo(chat_id=msg.from_user.id, photo=description_dict['image'])
            except WrongFileIdentifier:
                pass

        if 'name' in description_dict and 'definition' in description_dict:
            def_message = description_dict['name'].capitalize() + ' - ' + description_dict['definition']
            await bot.send_message(chat_id=msg.from_user.id, text=def_message)

        if 'morphology' in description_dict:
            morph = description_dict['morphology']

            # There are only 'adjective', 'adverb' and 'interjection' start with vowel sound
            if morph[0] in ('a', 'i'):
                morph_message = "It's an " + morph
            else:
                morph_message = "It's a " + morph

            await bot.send_message(chat_id=msg.from_user.id, text=morph_message)

        if 'pronunciations' in description_dict:
            pronoun = description_dict['pronunciations']
            # In case of single pronunciation availability
            if isinstance(pronoun, str):
                await bot.send_voice(chat_id=msg.from_user.id, voice=pronoun)
            else:
                await bot.send_voice(chat_id=msg.from_user.id, voice=pronoun['UK'],
                                     caption='British English pronunciation')
                await bot.send_voice(chat_id=msg.from_user.id, voice=pronoun['US'],
                                     caption='American English pronunciation')

        if 'examples' in description_dict:
            examples = description_dict['examples']

            if len(examples) == 1:
                examp_message = 'Example:\n1. ' + examples.pop()
            else:
                examp_message = 'Examples:\n1. ' + examples.pop() + '\n2. ' + examples.pop()

            await bot.send_message(chat_id=msg.from_user.id, text=examp_message)

    else:
        await bot.send_message(chat_id=msg.from_user.id, text=INVALID_INPUT_MESSAGE)


if __name__ == '__main__':
    print("Bot is currently running...\nTo stop press Ctrl+C")
    executor.start_polling(dp)
