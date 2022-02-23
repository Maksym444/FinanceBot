from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


button3 = KeyboardButton("💰 Ваш Кошелёк")
button4 = KeyboardButton("📥 Скачать введенные данные")
# button5 = KeyboardButton("✏️ Ввести данные")
button6 = KeyboardButton("🗿 Пользователи")
button7 = KeyboardButton("🗿 Активные пользователи")
button8 = KeyboardButton("🗿 Скачать пользователей")
button9 = KeyboardButton("⚙️ Настройки")
# button9 = KeyboardButton("🗿 Актив")

# Отчеты
button11 = KeyboardButton("🗓 Данные за всё время")
# button12 = KeyboardButton("🗓 Заработок за всё время")
# button13 = KeyboardButton("🗓 Траты за всё время")
button14 = KeyboardButton("🗓 Данные за семь дней")
button15 = KeyboardButton("🗓 Данные за тридцать дней")
button12 = KeyboardButton("📅 Выбрать диапазон для данных")
button16 = KeyboardButton("◀️ Назад в главное меню")
# Настройки
button17 = KeyboardButton("💰 Выбор валюты")
button18 = KeyboardButton("🕔 Выбрать время для вопроса")
button19 = KeyboardButton("⌛️ Выбрать день для отчета")
button20 = KeyboardButton("♾️ Выбрать регулярность отчетов")
button1 = KeyboardButton("📲 Поделиться контактом")
button2 = KeyboardButton("☎️ Удалить контакт")
button21 = KeyboardButton("🆘 Помощь")
button22 = KeyboardButton("👍 Поделиться ботом")

# Выбор валюты
button23 = KeyboardButton("💴 Гривна")
button24 = KeyboardButton("💵 Доллар")
button25 = KeyboardButton("💶️ Евро")
button26 = KeyboardButton("💷 Добавить свой вариант")
button27 = KeyboardButton("💰 Спрашивать меня о выборе валюты")
button28 = KeyboardButton("◀️ Назад в меню настроек")

button10 = KeyboardButton("❌ Отменить ввод")


markup_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_main_menu = markup_admin.add(button3).add(button4). \
            add(button6).add(button7).add(button8).add(button9)


markup_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user_main_menu = markup_user.add(button3).add(button4).add(button9)


markup_delete = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
delete = markup_delete.add(button10)

markup_report = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_report_menu = markup_report.add(button11).add(button12).add(button14).\
    add(button15).add(button16)

markup_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_menu = markup_settings.add(button17).add(button18).add(button19).add(button20).add(button21).add(button1).\
    add(button2).add(button22).add(button16)

markup_currency = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
currency_menu = markup_currency.add(button23).add(button24).add(button25).add(button26).add(button27).add(button28)



inline_btn_1 = InlineKeyboardButton('🧮 Ежемесячные платежи', callback_data='button1')
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_btn_2 = InlineKeyboardButton('🍱 Продукты', callback_data='button2')
inline_btn_3 = InlineKeyboardButton('🚗 Транспорт', callback_data='button3')
inline_btn_4 = InlineKeyboardButton('👕 Одежда', callback_data='button4')
inline_btn_5 = InlineKeyboardButton('🏡 Дом', callback_data='button5')
inline_btn_6 = InlineKeyboardButton('💊 Здоровье, красота', callback_data='button6')
inline_btn_7 = InlineKeyboardButton('📚 Образование', callback_data='button7')
inline_btn_8 = InlineKeyboardButton('💵 Доход', callback_data='button8')
inline_btn_9 = InlineKeyboardButton('🏝 Путешествия', callback_data='button9')
inline_btn_10 = InlineKeyboardButton('🏦 Отложенное', callback_data='button10')
inline_btn_11 = InlineKeyboardButton('🎭 Развлечения', callback_data='button11')
inline_btn_12 = InlineKeyboardButton('🎁 Подарки', callback_data='button12')
inline_btn_13 = InlineKeyboardButton('💻 Работа', callback_data='button13')
inline_btn_14 = InlineKeyboardButton('🤷 Другие траты', callback_data='button14')
category = inline_kb_full.add(inline_btn_2, inline_btn_3, inline_btn_4,
                              inline_btn_5, inline_btn_6, inline_btn_7,
                              inline_btn_8, inline_btn_9, inline_btn_10,
                              inline_btn_11, inline_btn_12, inline_btn_13)\
                    .add(inline_btn_14)



