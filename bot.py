# pylint: disable=C0114
from datetime import datetime, timedelta
import logging
import time
import asyncio
import aioschedule
from aiogram import Bot, Dispatcher, types
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode
import os

import config
import keybord
from config import API_TOKEN, admin
import keybord as kb
from db_set_schedule import question_time, get_question_time
from db_users import check_user, update_user_contact, update_user_activity, \
    check_phone, delete_phone, get_all_user_tg_id, take_user_reg_time
from db_admin import admin_user_to_exl, admin_show_user, \
    admin_show_user_activity
from db_expenditure import save_data
from db_wallet import show_wallet_info
from main_pdf import create_pdf_doc

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # memory storage for input data
dp = Dispatcher(bot, storage=storage)


# States for input data
class Form(StatesGroup):
    """States users data """
    quantity = State()  # Will be represented in storage as 'Form:quantity'
    category = State()  # Will be represented in storage as 'Form:category'
    annotation = State()  # Will be represented in storage as 'Form:annotation'


class Calendar(StatesGroup):
    """RANGE REPORT"""
    start_date = State()  # Will be represented in storage as 'Calendar:start_date'
    end_date = State()  # Will be represented in storage as 'Calendar:end_date'


class Question(StatesGroup):
    question_time = State()


class Currency (StatesGroup):
    currency = State()


def main_menu(user_id):
    if user_id == admin:
        return keybord.admin_main_menu
    else:
        return keybord.user_main_menu


def report_menu():
    return keybord.markup_report_menu


def settings():
    return keybord.settings_menu


def currency():
    return keybord.currency_menu


# MAIN MENU
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    """ This handler will be called when user sends `/start` command. It will
     check user in db, if user doesn't exist: he will be written in the db and
     the wallet will be created. If the user exist he will be answered, welcome back.
     In check_user function you can set admin tg_id, and that user will become an admin,
     with opportunity to get information about users. """
    await bot.send_message(config.admin, f'Новый пользователь! '
    f'{message.from_user["id"],message.from_user["username"], message.from_user["first_name"], message.from_user["language_code"]}')
    await message.answer(check_user(message.from_user, date=d), reply_markup=main_menu(message.from_user['id']))


@dp.message_handler(state='*', commands='❌ Отменить ввод')
# You can use state '*' if you need to handle all states
@dp.message_handler(Text(equals='❌ Отменить ввод', ignore_case=True), state='*')
# текст который равен "cancel", игнорировать регистр, для всех стейтов
async def cancel_handler(message: types.Message, state: FSMContext):
    """ This handlers will be stop input of any data if word cancel will be typed.
    Allow user to cancel any action"""
    current_state = await state.get_state()  # я правильно понимаю что это встроенная функция
    if current_state is None:
        return
    logging.warning('Cancelling state %r', current_state)  # Cancel state and inform user about it
    await state.finish()
    await message.bot.send_message(message.chat.id, 'Ввод данных отменен!')
    # And remove keyboard (just in case)


@dp.message_handler(regexp='[0-9]+')
async def quantity(message: types.Message, state: FSMContext):
    """ This handler will be called when user sends `/transaction` command.
     Will set State quantity"""
    await Form.quantity.set()
    # if int(message.text) > 0:
    await state.update_data(quantity=message.text)
    await Form.next()
    await bot.send_message(message.chat.id, 'Записали!',
                           reply_markup=types.ReplyKeyboardRemove() and keybord.delete)
    await message.answer("Теперь выберите категорию в которую внести данные!",
                         reply_markup=keybord.category)
    # elif int(message.text) == 0:
    #     await message.reply("Введенная Вами сумма не может быть равна 0!")
    # else:
    #     await message.reply("Введенная Вами сумма не может иметь минусовые значения!")


@dp.callback_query_handler(Text(equals=['button1']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Ежемесячные платежи"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!', reply_markup=None)


@dp.callback_query_handler(Text(equals=['button2']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Продукты"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!', reply_markup=None)


@dp.callback_query_handler(Text(equals=['button3']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery,state: FSMContext):
    category = "Транспорт"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button4']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery,state: FSMContext):
    category = "Одежда"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button5']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Дом"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button6']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Здоровье, красота"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button7']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Образование"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button8']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Доход"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button9']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Путешествия"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button10']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Отложенное"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button11']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Развлечения"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button12']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Подарки"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button13']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Работа"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.callback_query_handler(Text(equals=['button14']), state=Form.category)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    category = "Другие траты"
    await Form.next()
    await state.update_data(category=category)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    time.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Введите аннотацию к сумме!')


@dp.message_handler(state=Form.annotation)
async def annotation_add(message: types.Message, state: FSMContext):
    """ This handler will save State annotation and ask for next handler and work with him"""
    async with state.proxy() as data:
        now = datetime.now()
        d = now.strftime('%Y-%m-%d %H:%M:%S')
        data['annotation'] = message.text
        if data['category'] == 'Доход':
            data['vector'] = True
        else:
            data['vector'] = False
        print(data['quantity'], data['category'], data['vector'], data['annotation'])
        save_data(message.chat.id, data['quantity'], data['category'], data['annotation'],
                  data['vector'], d)
        markup1 = types.ReplyKeyboardRemove()  # Remove keyboard
        await bot.send_message(  # And send message
            message.chat.id,
            md.text(
                md.text('Сумма: ', md.bold(data['quantity'])),
                md.text('Категория: ', md.code(data['category'])),
                md.text('Аннотация: ', md.code(data['annotation'])),
                sep='\n',  # разделитель с новой строчки
            ),
            reply_markup=markup1 and main_menu(message.from_user['id']),
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()  # Finish conversation


@dp.message_handler(Text(equals="💰 Ваш Кошелёк"))
async def bank_account(message: types.Message):
    """ This handler will be called when user sends `/bank_account` command.
        Will send information about money quantity on user's wallet"""
    user_id = message.from_user
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    update_user_activity(tg_id=message.from_user['id'], date=d)
    await message.answer(show_wallet_info(user_id))


@dp.message_handler(Text(equals="📥 Скачать введенные данные"))
async def notes(message: types.Message):
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    user_id = message.from_user
    update_user_activity(tg_id=user_id['id'], date=d)
    await message.answer("Выберете вид отчета", reply_markup=report_menu())
    """ This handler will be called when user sends `/notes` command.
        Will send xlsx file with all transaction"""


# MENU SETTINGS
@dp.message_handler(Text(equals="⚙️ Настройки"))
async def notes(message: types.Message):
    user_id = message.from_user
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    update_user_activity(tg_id=user_id['id'], date=d)
    await message.answer("Выберете настройки", reply_markup=settings())
    """ This handler will be called when user sends `/notes` command.
        Will send xlsx file with all transaction"""


@dp.message_handler(Text(equals="💰 Выбор валюты"))
async def notes(message: types.Message):
    user_id = message.from_user
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    update_user_activity(tg_id=user_id['id'], date=d)
    await message.answer("Выберете валюту", reply_markup=currency())
    """ This handler will be called when user sends `/notes` command.
        Will send xlsx file with all transaction"""


# MENU REPORT
@dp.message_handler(Text(equals="🗓 Данные за всё время"))
async def all_time(message: types.Message):
    user_id = message.from_user
    tg_id = user_id['id']
    start_date = take_user_reg_time(tg_id)
    now = datetime.now() + timedelta(days=1)
    end_date = now.strftime("%d.%m.%Y")
    if check_phone(tg_id, start_date, end_date) is None:
        await message.answer("У Вас пока ничего нет")
    else:
        if not check_phone(tg_id, start_date, end_date):
            await message.answer(
                "Неполный функционал, необходимо добавить номер. "
                "\n Для этого добавьте номер телефона. \n"
                "Его можна удалить, если Вы перестанете пользоваться сервисом")
        else:
            await message.answer(check_phone(tg_id, start_date, end_date))
            time.sleep(2)
            with open(f'./files/{tg_id}/{start_date[:10]}-{end_date[:10]}.pdf', 'rb') as doc:
                await message.reply_document(doc)


@dp.message_handler(Text(equals="🗓 Данные за семь дней"))
async def all_time(message: types.Message):
    user_id = message.from_user
    tg_id = user_id['id']
    now = datetime.now() + timedelta(days=1)
    term_now = now.strftime("%d.%m.%Y")
    d = datetime.now() - timedelta(days=7)
    past = d.strftime("%d.%m.%Y")
    if check_phone(tg_id, past, term_now) is None:
        await message.answer("У Вас пока ничего нет")
    else:
        if not check_phone(tg_id, past, term_now):
            await message.answer(
                "Неполный функционал, необходимо добавить номер. "
                "\n Для этого добавьте номер телефона. \n"
                "Его можна удалить, если Вы перестанете пользоваться сервисом")
        else:
            await message.answer(check_phone(tg_id, past, term_now))
            time.sleep(2)
            with open(f'./files/{tg_id}/{past[:10]}-{term_now[:10]}.pdf', 'rb') as doc:
                await message.reply_document(doc)


@dp.message_handler(Text(equals="🗓 Данные за тридцать дней"))
async def all_time(message: types.Message):
    user_id = message.from_user
    tg_id = user_id['id']
    now = datetime.now() + timedelta(days=1)
    term_now = now.strftime("%d.%m.%Y")
    d = datetime.now() - timedelta(days=30)
    past = d.strftime("%d.%m.%Y")
    if check_phone(tg_id, past, term_now) is None:
        await message.answer("У Вас пока ничего нет")
    else:
        if not check_phone(tg_id, past, term_now):
            await message.answer(
                "Неполный функционал, необходимо добавить номер. "
                "\n Для этого добавьте номер телефона. \n"
                "Его можна удалить, если Вы перестанете пользоваться сервисом")
        else:
            await message.answer(check_phone(tg_id, past, term_now))
            time.sleep(2)
            with open(f'./files/{tg_id}/{past[:10]}-{term_now[:10]}.pdf', 'rb') as doc:
                await message.reply_document(doc)


@dp.message_handler(Text(equals="🕔 Выбрать время для вопроса"))
async def cmd_add(message: types.Message):
    """ SET DATE FOR RANGE """
    await Question.question_time.set()
    await bot.send_message(message.chat.id, "Введите время в формате 18:00 для выбора времени вопроса")


@dp.message_handler(state=Question.question_time)
async def annotation_add(message: types.Message, state: FSMContext):
    """ SET DATE FOR RANGE """
    data = message.text
    try:
        question_time(data, message.chat.id)
        await bot.send_message(message.chat.id, f"Теперь бот будет Вас спрашивать в {data}.")
    except ValueError:
        return await message.reply("Пожалуйста, введите в верном формате: 18:00")


@dp.message_handler(Text(equals="📅 Выбрать диапазон для данных"))
async def cmd_add(message: types.Message):
    """ SET DATE FOR RANGE """
    await Calendar.start_date.set()
    await bot.send_message(message.chat.id, "Введите начальную дату в формате день.месяц.год (22.11.2021)",
                           reply_markup=types.ReplyKeyboardRemove() and keybord.delete)
    # await bot.send_message(message.chat.id, "Выберите диапазон",
    #                        reply_markup=keybord.markup_report_menu)


@dp.message_handler(state=Calendar.start_date)
async def annotation_add(message: types.Message, state: FSMContext):
    """ SET DATE FOR RANGE """
    data = message.text
    now = datetime.now()
    try:
        entire_date = datetime.strptime(data, '%d.%m.%Y')
        if entire_date > now:
            return await message.reply("Вы ввели дату больше чем сегодняшняя!")
        else:
            async with state.proxy() as data:
                data['calendar_start_date'] = message.text
            await Calendar.next()
            await bot.send_message(message.chat.id, "Введите конечную дату в формате день.месяц.год (22.11.2021)")
    except ValueError:
        return await message.reply("Пожалуйста, введите в верном формате: 11.12.2021")


@dp.message_handler(state=Calendar.end_date)
async def annotation_add(message: types.Message, state: FSMContext):
    """ SET DATE FOR RANGE """
    data = message.text
    now = datetime.now() + timedelta(days=1)
    try:
        entire_date = datetime.strptime(data, '%d.%m.%Y')
        if entire_date > now:
            return await message.reply("Вы ввели дату больше чем сегодняшняя!")
        else:
            async with state.proxy() as data:
                data['calendar_end_date'] = message.text
                term_now = data['calendar_end_date']
                past = data['calendar_start_date']
                create_pdf_doc(message.chat.id, past, term_now)
                await bot.send_message(message.chat.id, "Подождите!", reply_markup=kb.markup_report)
                path = f'./files/{message.chat.id}/{past}-{term_now}.pdf'
                with open(path, 'rb') as doc:
                    await message.reply_document(doc)
                os.remove(path)
            await state.finish()
    except ValueError:
        return await message.reply("Пожалуйста, введите в верном формате: 11.12.2021")


@dp.message_handler(Text(equals="◀️ Назад в главное меню"))
async def all_time(message: types.Message):
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    user_id = message.from_user
    tg_id = user_id['id']
    update_user_activity(tg_id=user_id['id'], date=d)
    await message.answer("Возвращайтесь позже", reply_markup=main_menu(tg_id))


@dp.message_handler(Text(equals="◀️ Назад в меню настроек"))
async def all_time(message: types.Message):
    now = datetime.now()
    d = now.strftime('%Y-%m-%d %H:%M:%S')
    user_id = message.from_user
    tg_id = user_id['id']
    update_user_activity(tg_id=user_id['id'], date=d)
    await message.answer("Возвращайтесь позже", reply_markup=settings())


@dp.message_handler(Text(equals="📲 Поделиться контактом"))
async def get_con(message: types.Message):
    """ This handler will ask for phone number"""
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
    await message.answer("Поделитесь Вашим контактом!", reply_markup=markup_request)


@dp.message_handler(content_types=['contact'])
async def contact(message):
    """ This handler will save phonenumber and update db"""
    if message.contact is not None:
        keyboard = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, 'Вы успешно отправили свой номер',
                               reply_markup=main_menu(message.from_user['id']))
        data = dict(message.contact)
        tg_id = data['user_id']
        phone_number = data['phone_number']
        return update_user_contact(tg_id, phone_number)


@dp.message_handler(Text(equals="☎️ Удалить контакт"))
async def delete_contact(message: types.Message):
    """ This handler will delete phonenumber and update db"""
    await message.answer(delete_phone(message.from_user['id']))


#ADMIN MENU
@dp.message_handler((Text(equals="🗿 Скачать пользователей")))
async def admin_download(message: types.Message):
    """ This handler will save to xlsx all information about users and send it to admin"""
    admin_user_to_exl(message.from_user['id'])
    doc = open('./admin_files/users.xlsx', 'rb')
    await message.reply_document(doc)


@dp.message_handler((Text(equals="🗿 Пользователи")))
async def users(message: types.Message):
    """ This handler will show all user in row data"""
    await message.answer(admin_show_user(message.from_user['id']))


@dp.message_handler((Text(equals="🗿 Активные пользователи")))
async def active_users(message: types.Message):
    """ This handler will show all active user in row data"""
    await message.answer(admin_show_user_activity(message.from_user['id']))


async def ask_question():
    """schedule timing"""
    for elem in get_all_user_tg_id():
        await bot.send_message(elem, "Если у Вас есть данные введите их.")


# async def say():
#     for elem in get_all_user_tg_id():
#         if info_week_user_to_exl(tg_id=elem) is None:
#             await bot.send_message("У Вас ничего нет", elem)
#         else:
#             with open(f'./files/{elem}/info-week-{elem}' + '.xlsx', 'rb') as doc1:
#                 await bot.send_document(elem, doc1)


# def set_question_time():
#     a = get_all_user_tg_id()
#     for elem in a:
#         return get_question_time(elem)


async def scheduler():
    """scheduler"""
    aioschedule.every().day.at("16:50").do(ask_question)
    # aioschedule.every(int(set_answer_regular())).days.at(set_question_time()).do(say)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    """end schedule timing"""
    asyncio.create_task(scheduler())




