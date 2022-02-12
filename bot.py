# -*- coding: utf-8 -*-

# AIOGRAM
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import Throttled
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, reply_keyboard
from aiogram.utils import executor
import aiogram.utils
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from mod.api import API
from PIL import Image, ImageDraw, ImageFont
import random, os, textwrap
from mod.data import stat

work = 0
font = ImageFont.truetype("files/JetBrainsMono-Bold.ttf", 16, encoding="unic")

bot_token = ''
bot = Bot(token=bot_token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("👮 Не спамь!")

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply('🐍 Запускайте код python(остальное в разработке) в нашем боте!\n\nИнформация и иснструкция по команде /help\nСписок установленных библиотек: /libs', parse_mode='html')

# /help
@dp.message_handler(commands=['help'])
async def send_helpe(message: types.Message):
	await message.reply('🐍 Так, <b>всё супер легко</b>, пришли боту код на <b>python</b>(<u>в чатах надо отвечать на сообщнение</u>), подожди, и получи результат!\n<b>Обозначения:</b>\n 🔴^C - команда остановлена ошибкой или ограничением по времени\n\n<i>Ограничения для выпоняемого кода: 5 секунд, cpus 0.1, 50 MB оперативной памяти, отключен интернет(в будующем возможны привилегии)</i>', parse_mode='html')

# /libs
@dp.message_handler(commands=['libs'])
async def send_libs(message: types.Message):
	f = open('requirements.txt','r')
	await message.reply(f'🐍 <b>requirements.txt</b>\n{f.read()}', parse_mode='html')
	f.close()

# /stat
@dp.message_handler(commands=['stat'])
async def send_stat(message: types.Message):
	pc = stat()
	await message.reply(f'''
{pc["status"]["cpu"]} <b>CPU:</b> <code>{pc['cpu']['used']} / {pc['cpu']['total']}</code> <i>({pc["cpu"]["percent"]}%)</i>
{pc["status"]["memory"]} <b>Memory:</b> <code>{pc['memory']['used']} MiB /{pc['memory']['total']} MiB</code> <i>({pc["memory"]["percent"]}%)</i>
{pc["status"]["disk"]} <b>Disk: </b> <code>{pc['disk']['used']} MiB /{pc['disk']['total']} MiB</code> <i>({pc["disk"]["percent"]}%)</i>
''', parse_mode='html')

@dp.message_handler(content_types=["text"])
@dp.throttled(anti_flood, rate=5)
async def check(message: types.Message):
	global work
	try:
		work += 1
		res = API.start(message.text, 'py')
		if res["result"]:
			work -= 1
		if work <= 20:
			print(f'{res["code"]} - @{message.from_user.username}')
			string = f'<code>{res["code"].replace("<", "&lt;")}</code>\n\n<b>Result:</b>\n<code>{res["result"].replace("<", "&lt;")}</code>\n<b>Usage:</b>\n 💽 <b>Memory:</b> {res["usage"]["memory"]} / {res["max"]["memory"]}\n 🕐 <b>Time:</b> {res["usage"]["time"]} / {res["max"]["time"]}'
			#leng = 3000
			#if len(string) < 3000: leng = len(string)
			#num = random.randrange(1, 999999999999999)
			#image = Image.new("RGB", (1000, 800), "#2c0821")
			#draw = ImageDraw.Draw(image)
			#draw.text((10, 5), "vsecodertester", fill='#7fc930', font=font)
			#draw.text((150, 5), ":", fill='white', font=font)
			#draw.text((165, 5), "~", fill='#617aa5', font=font)
			#draw.text((185, 5), "$ python script.py", fill='white', font=font)
			#y = 25
			#m = 0
			#for text in res["result"][0:leng].split('\n'):
			#	ress = ''
			#	text = textwrap.wrap(text, width=100)
			#	for t in text:
			#		ress += t + '\n'
			#		m += 20
			#	draw.text((10, y), f'{ress}', fill='white', font=font)
			#	y += m
			#	m = 0
			#print(res["status"])
			#if res["usage"]["memory"] == '... MiB':
			#	draw.text((500, 5), "^C", fill='red', font=font)
			#image.save(f'{num}.png')
			#string = f'<code>{res["code"].replace("<", "&lt;")}</code>\n\n<b>Result:</b> Look up =)\n\n<b>Usage:</b>\n 💽 <b>Memory:</b> {res["usage"]["memory"]} / {res["max"]["memory"]}\n 🕐 <b>Time:</b> {res["usage"]["time"]} / {res["max"]["time"]}'
			#await bot.send_photo(message.chat.id, open(f'{num}.png', 'rb'), caption=string, parse_mode="html")
			#os.remove(f'{num}.png')
			await bot.send_message(message.chat.id, string, parse_mode="html")
		else:
			await message.reply('😔 Больше 20 процессов выполняется на сервере, пожалуйста попробуйте позже!')
	except Exception as e:
		try:
			string = f'<code>{res["code"].replace("<", "&lt;")}</code>\n\n<b>Result:</b>\n<code>{res["result"].replace("<", "&lt;")}</code>\n<b>Usage:</b>\n 💽 <b>Memory:</b> {res["usage"]["memory"]} / {res["max"]["memory"]}\n 🕐 <b>Time:</b> {res["usage"]["time"]} / {res["max"]["time"]}'
			leng = 3000
			if len(string) < 3000: leng = len(string)
			num = random.randrange(1, 999999999999999)
			image = Image.new("RGB", (1000, 800), "#2c0821")
			draw = ImageDraw.Draw(image)
			draw.text((10, 5), "vsecodertester", fill='#7fc930', font=font)
			draw.text((150, 5), ":", fill='white', font=font)
			draw.text((165, 5), "~", fill='#617aa5', font=font)
			draw.text((185, 5), "$ python script.py", fill='white', font=font)
			y = 25
			m = 0
			for text in res["result"][0:leng].split('\n'):
				ress = ''
				text = textwrap.wrap(text, width=100)
				for t in text:
					ress += t + '\n'
					m += 20
				draw.text((10, y), f'{ress}', fill='white', font=font)
				y += m
				m = 0
			print(res["status"])
			if res["usage"]["memory"] == '... MiB':
				draw.text((500, 5), "^C", fill='red', font=font)
			image.save(f'{num}.png')
			string = f'<code>{res["code"].replace("<", "&lt;")}</code>\n\n<b>Usage:</b>\n 💽 <b>Memory:</b> {res["usage"]["memory"]} / {res["max"]["memory"]}\n 🕐 <b>Time:</b> {res["usage"]["time"]} / {res["max"]["time"]}'
			await bot.send_photo(message.chat.id, open(f'{num}.png', 'rb'), caption=string, parse_mode="html")
			os.remove(f'{num}.png')
		except:
			await bot.send_message(message.chat.id, 'Не получилось отправить результат, он слишком большой, а боту не разрешено отправлять фото\n------------------------------------------\nIt was not possible to send the result, it is too big, and the bot is not allowed to send photos', parse_mode="html")

if __name__ == "__main__":
	executor.start_polling(dp)
