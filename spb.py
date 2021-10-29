from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
import os, time, asyncio, datetime
from threading import Thread

button_info = KeyboardButton('ℹ️Условия сотрудничестваℹ️')
button_go = KeyboardButton('🔥Приступить к работе🔥')
button_share = KeyboardButton('🗣️Пригласить друга🗣️')
button_rate = KeyboardButton('⭐Рейтинг⭐')
button_help = KeyboardButton('🙏Помощь🙏')
button_rules = KeyboardButton('📖Работа с сервисом📖')
button_billing = KeyboardButton('🧾Юр. информация🧾')
button_back = KeyboardButton('↩️Назад↩️')
main_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
main_kb.add(button_info)
main_kb.add(button_go)
main_kb.add(button_share)
main_kb.row(button_rate, button_help)
info_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
info_kb.add(button_rules)
info_kb.add(button_billing)
info_kb.add(button_back)
memory_storage = MemoryStorage()
TOKEN = "1956727734:AAHm4PPZBtPbczwiL4ENhN3Q0VEITukT-ps"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
buy_callback = CallbackData("item_name", "sub")
task = ""
sub = ""
state = "none"
chat_id = -1001548837699
if(not os.path.exists('settings')):
   os.mkdir('settings')
   open('settings/tasknumber.txt', 'x').write("1")
if(not os.path.exists('tasks')):
   os.mkdir('tasks')
if(not os.path.exists('users')):
   os.mkdir('users')

async def on_shutdown(dp):
    await bot.close()

@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
   # try:
      #await msg.answer("Мы здесь [СпецПрофи](https://t.me/joinchat/SrR3PhtTmHExNzUy)", parse_mode='markdown')
      if(not os.path.exists('users/'+str(msg["from"].id))):
         os.mkdir('users/'+str(msg["from"].id))
         open('users/'+str(msg["from"].id)+'/rating.txt', 'x').write("0")
      await msg.reply("Здравствуйте!\nЯ Бот сервиса «СпецПрофи»\nОзнакомьтесь с условиями сотрудничества и жмите «Перейти в чат»\nХорошей работы!👍🏻",reply_markup=main_kb)
   # except:
      # return
    
@dp.message_handler(commands=['task'])
async def send_welcome(msg: types.Message):
   # try:
      is_admin = False
      for admin in await bot.get_chat_administrators(chat_id):
         if(msg["from"].id == admin["user"].id):
            is_admin = True
      if(is_admin):
         num = open('settings/tasknumber.txt', 'r').read()
         sub = '🛠🙋🏻‍♂️Задание номер: '+num+"\n"+str(msg.text).replace("&&&","")[6:]
         txt = '🛠🙋🏻‍♂️Задание номер: '+num+"\n"+str(msg.text)[:msg.text.find("&&&")][6:]
         # name = str(msg.date).replace("-","").replace(" ","").replace(":","")
         name = num
         os.mkdir('tasks/'+name)
         open('tasks/'+name+"/text.txt", 'w').write(msg.text+":::"+str(msg["from"].id))
         cbd = "select:"+name
         await bot.send_message(chat_id, text=txt ,reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
         await msg.answer("Задание опубликованно")
         open('settings/tasknumber.txt', 'w').write(str(int(num)+1))
         # await msg.answer("[Создать задание]()")
   # except:
      # return

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
   if(msg.text=='ℹ️Условия сотрудничестваℹ️'):
      temp_msg = await msg.reply("Секундочку...",reply_markup=info_kb)
   if(msg.text=='📖Работа с сервисом📖'):
      await msg.reply("""
👋🏻Приветствуем Вас мастера!
Это чат с заказами по Москве! Сантехника, электрика, муж на час, мелкий ремонт, сборка мебели, ремонт техники, отделочные работы и многое разное.
Условия работы с сервисом:
1.Соблюдение и ответственное исполнение договоренностей с клиентом (влияет на ваш рейтинг)
2.Корректное общение с администацией чата (по возникшим вопросам)
3.Оплата фиксированной суммы (далее "Партнерский взнос") в размере 90 рублей.
Оплата произволится на условиях предоставления
информации (имя, адрес, номер телефона) заказчика.

Схема работы:
1.В чате отображается новая заявка от клиента с кнопкой "Я БЕРУ"
2.Берете заявку, если вам подходит.
3.Оплачиваете "Партнерский взнос"
4.Связываетесть с клиентом и договариваетесть о времени и суммме работы.
5.Если договорились - жмете "В РАБОТЕ". Заявка скрывается из общего чата и закрепляется за Вами автоматически повышая Ваш рейтинг.
Дополнение* - заявка доступна первым 3-м мастерам одновременно.

Уважаемый мастер! Партнерский взнос составляет 90 рублей. После оплаты Вам будет доступна вся информация для связи с заказчиком (имя,адрес,номер телефона)

Хорошей работы!🤝
По всем вопросам- АДМИН  @staslev1""", reply_markup=info_kb)
   if(msg.text=='🧾Юр. информация🧾'):
      await msg.reply("""
111674, Россия, Москва. ул,Открытое шоссе 6 к11 кв 39
Email: comfort.2ч4@mail.ru
Tel: +79990402423
ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ ЛЕВЧЕНКО СТАНИСЛАВ ДМИТРИЕВИЧ,
ИНН
253501674317,
ОГРН
321253600078420
Юридический адрес организации
692361, РОССИЯ, ПРИМОРСКИЙ КРАЙ, ЯКОВЛЕВСКИЙ Р-Н, СЕЛО ЯКОВЛЕВКА, ПОЧТОВЫЙ ПЕР, Д 31""", reply_markup=info_kb)
   if(msg.text=='🗣️Пригласить друга🗣️'):
      temp_msg = await msg.reply("Привет! Есть отличный сервис где можно взять заказ. Вот ссылка @SpetsProfiBot переходи и жми Start", reply_markup=main_kb)
   if(msg.text=='⭐Рейтинг⭐'):
      await msg.reply("Система рейтинга находится в разработке.", reply_markup=main_kb)
   if(msg.text=='🙏Помощь🙏'):
      await msg.reply("По любым вопросом обращайтесь сюда: @staslev1\nПожалуйста, перед тем как обращаться за помощью к администрации, убедитесь\nчто ваш вопрос действительно требует внимания и ответа на него нет в разделе 📖Правила📖 или закрепленном сообщении.", reply_markup=main_kb)
   if(msg.text=='↩️Назад↩️'):
      temp_msg = await msg.reply("Секундочку...",reply_markup=main_kb)
   if(msg.text=='💰Приступить к работе💰'):
      await msg.answer("Все заказы по москве мы размещаем здесь:\n[СпецПрофи](https://t.me/joinchat/SrR3PhtTmHExNzUy)", parse_mode='markdown', reply_markup=main_kb)


@dp.callback_query_handler(text_contains="select")
async def selecting(call: CallbackQuery):
   # try:
      callback_data = call.data
      dt = text=open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      cbd = "cancel:"+callback_data[7:]
      msg = await bot.send_message(call["from"].id, dt.replace("&&&","")[6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Выполненно", callback_data="finish:"+callback_data[7:])).insert(InlineKeyboardButton(text="Отказаться", callback_data=cbd)))
      open('tasks/'+callback_data[7:]+"/msgid", 'w').write(str(msg.message_id))
      await call["message"].delete()
      name = ""
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="\["+str(call["from"].id)+"]\n["+name+"](tg://user?id="+str(call["from"].id)+")"+"\nВзял задание номер: "+callback_data[7:], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Забрать", callback_data="depriv:"+callback_data[7:])), parse_mode='markdown')
      #await waitedmsg(10, str(call["from"].id))
   # except:
      # return

@dp.callback_query_handler(text_contains="cancel")
async def canceltask(call: CallbackQuery):
   try:
      await call["message"].delete()
      callback_data = call.data
      txt = open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      cbd = "select:"+callback_data[7:]
      dt = text=open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(chat_id, text=txt[:txt.find("&&&")][6:dt.find(":::")-3] ,reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
      await bot.send_message(dt[dt.find(":::")+3:], text="\["+str(call["from"].id)+"]\n["+name+"](tg://user?id="+str(call["from"].id)+")"+"\nОтказался от задания номер: "+callback_data[7:], parse_mode='markdown')
   except:
      return

@dp.callback_query_handler(text_contains="finish")
async def finishtask(call: CallbackQuery):
   # try:
      await call["message"].edit_reply_markup(reply_markup=InlineKeyboardMarkup())
      callback_data = call.data
      cbd = "resend:"+callback_data[7:]
      dt = text=open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="\["+str(call["from"].id)+"]\n["+name+"](tg://user?id="+str(call["from"].id)+")"+"\nВыполнил задание номер: "+callback_data[7:], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Вернуть в оборот", callback_data=cbd)), parse_mode='markdown')
      os.remove(callback_data[7:])
   # except:
      # return

@dp.callback_query_handler(text_contains="depriv")
async def canceltask(call: CallbackQuery):
   # try:
      callback_data = call.data
      txt = open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      msgid = open('tasks/'+callback_data[7:]+"/msgid", 'r').read()
      cbd = "select:"+callback_data[7:]
      dt = text=open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      await bot.delete_message(call["message"].text[call["message"].text.find("[")+1:call["message"].text.find("]")],msgid)
      await call["message"].edit_reply_markup(reply_markup=InlineKeyboardMarkup())
      await bot.send_message(chat_id, text=txt[:txt.find("&&&")][6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="Вы забрали задание у ["+call["message"].text[call["message"].text.find("\n")+1:call["message"].text.find("\n").find("\n")]+"](tg://user?id="+call["message"].text[call["message"].text.find("[")+1:call["message"].text.find("]")]+")\n"+dt.replace("&&&","")[6:dt.find(":::")-3], parse_mode='markdown')
   # except:
      # return

@dp.callback_query_handler(text_contains="resend")
async def canceltask(call: CallbackQuery):
   # try:
      callback_data = call.data
      txt = open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      cbd = "select:"+callback_data[7:]
      dt = text=open('tasks/'+callback_data[7:]+"/text.txt", 'r').read()
      await call["message"].edit_reply_markup(reply_markup=InlineKeyboardMarkup())
      await bot.send_message(chat_id, text=txt[:txt.find("&&&")][6:dt.find(":::")-3], reply_markup=InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text="Я беру", callback_data=cbd)))
      if(call["from"].last_name):
         name = call["from"].first_name+" "+call["from"].last_name
      else:
         name = call["from"].first_name
      await bot.send_message(dt[dt.find(":::")+3:], text="Вы вернули задание в оборот.\n"+dt.replace("&&&","")[6:dt.find(":::")-3], parse_mode='markdown')
   # except:
      # return

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
