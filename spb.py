from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
import os, time, asyncio, datetime
from threading import Thread

memory_storage = MemoryStorage()
TOKEN = "1956727734:AAHm4PPZBtPbczwiL4ENhN3Q0VEITukT-ps"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
buy_callback = CallbackData("item_name", "sub")
task = ""
sub = ""
state = "none"
chat_id = -1001548837699

async def on_shutdown(dp):
    await bot.close()

@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
   try:
      await msg.answer("Мы здесь [СпецПрофи](https://t.me/joinchat/SrR3PhtTmHExNzUy)", parse_mode='markdown')
   except:
      return
    
@dp.message_handler(commands=['task'])
async def send_welcome(msg: types.Message):
   try:
      is_admin = False
      for admin in await bot.get_chat_administrators(chat_id):
         if(msg["from"].id == admin["user"].id):
            is_admin = True
      if(is_admin):
         sub = str(msg.text).replace("&&&","")[6:]
         txt = str(msg.text)[:msg.text.find("&&&")][6:]
         name = str(msg.date).replace("-","").replace(" ","").replace(":","")
         os.mkdir(name)
         open(name+"/text.txt", 'w').write(msg.text+":::"+str(msg["from"].id))
         cbd = "select:"+name
         await bot.send_message(chat_id, text=txt ,reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
         await msg.answer("Задание опубликованно")
         # await msg.answer("[Создать задание]()")
   except:
      return

# @dp.message_handler(content_types=['text'])
# async def get_text_messages(msg: types.Message):
#    return

@dp.callback_query_handler(text_contains="select")
async def selecting(call: CallbackQuery):
   try:
      callback_data = call.data
      dt = text=open(callback_data[7:]+"/text.txt", 'r').read()
      cbd = "cancel:"+callback_data[7:]
      msg = await bot.send_message(call["from"].id, dt.replace("&&&","")[6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Выполненно", callback_data="finish:"+callback_data[7:])).insert(InlineKeyboardButton(text="Отказаться", callback_data=cbd)))
      open(callback_data[7:]+"/msgid", 'w').write(str(msg.message_id))
      await call["message"].delete()
      name = ""
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="\["+str(call["from"].id)+"]\n["+name+"](tg://user?id="+str(call["from"].id)+")"+"\nВзял задание:\n"+dt.replace("&&&","")[6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Забрать", callback_data="depriv:"+callback_data[7:])), parse_mode='markdown')
      # await waitedmsg(10, str(call["from"].id))
   except:
      return

@dp.callback_query_handler(text_contains="cancel")
async def canceltask(call: CallbackQuery):
   try:
      await call["message"].delete()
      callback_data = call.data
      txt = open(callback_data[7:]+"/text.txt", 'r').read()
      cbd = "select:"+callback_data[7:]
      dt = text=open(callback_data[7:]+"/text.txt", 'r').read()
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(chat_id, text=txt[:txt.find("&&&")][6:dt.find(":::")-3] ,reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
      await bot.send_message(dt[dt.find(":::")+3:], text="\["+str(call["from"].id)+"]\n["+name+"](tg://user?id="+str(call["from"].id)+")"+"\nОтказался от задания:\n"+dt.replace("&&&","")[6:dt.find(":::")-3], parse_mode='markdown')
   except:
      return

@dp.callback_query_handler(text_contains="finish")
async def finishtask(call: CallbackQuery):
   try:
      await call["message"].edit_reply_markup(reply_markup=InlineKeyboardMarkup())
      callback_data = call.data
      cbd = "resend:"+callback_data[7:]
      dt = text=open(callback_data[7:]+"/text.txt", 'r').read()
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="\["+str(call["from"].id)+"]\n["+name+"](tg://user?id="+str(call["from"].id)+")"+"\nВыполнил задание:\n"+dt.replace("&&&","")[6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Вернуть в оборот", callback_data=cbd)), parse_mode='markdown')
      os.remove(callback_data[7:])
   except:
      return

@dp.callback_query_handler(text_contains="depriv")
async def canceltask(call: CallbackQuery):
   try:
      callback_data = call.data
      txt = open(callback_data[7:]+"/text.txt", 'r').read()
      msgid = open(callback_data[7:]+"/msgid", 'r').read()
      cbd = "select:"+callback_data[7:]
      dt = text=open(callback_data[7:]+"/text.txt", 'r').read()
      await bot.delete_message(call["message"].text[call["message"].text.find("[")+1:call["message"].text.find("]")],msgid)
      await call["message"].edit_reply_markup(reply_markup=InlineKeyboardMarkup())
      await bot.send_message(chat_id, text=txt[:txt.find("&&&")][6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="Вы забрали задание у ["+call["message"].text[call["message"].text.find("\n")+1:call["message"].text.find("\n").find("\n")]+"](tg://user?id="+call["message"].text[call["message"].text.find("[")+1:call["message"].text.find("]")]+")\n"+dt.replace("&&&","")[6:dt.find(":::")-3], parse_mode='markdown')
   except:
      return

@dp.callback_query_handler(text_contains="resend")
async def canceltask(call: CallbackQuery):
   try:
      callback_data = call.data
      txt = open(callback_data[7:]+"/text.txt", 'r').read()
      cbd = "select:"+callback_data[7:]
      dt = text=open(callback_data[7:]+"/text.txt", 'r').read()
      await call["message"].edit_reply_markup(reply_markup=InlineKeyboardMarkup())
      await bot.send_message(chat_id, text=txt[:txt.find("&&&")][6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="Вы вернули задание в оборот.\n"+dt.replace("&&&","")[6:dt.find(":::")-3], parse_mode='markdown')
   except:
      return

def timer(time, id):
   print("timer")
   asyncio.run(waitedmsg(time, id))

async def waitedmsg(time, id):
   while datetime.datetime.now()<=datetime.datetime.now()+datetime.timedelta(seconds = 10):
      pass
   await bot.send_message(id, text="Вы связались с заказчиком?", parse_mode='markdown')

if __name__ == '__main__':
   print("Бот запущен, все ОК")
   executor.start_polling(dp, on_shutdown=on_shutdown)
