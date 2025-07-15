from aiogram import types


markup_reply_one = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Моя таблица')
item2 = types.KeyboardButton('Создать новую')
item3 = types.KeyboardButton('Отменить добавление таблицы')
markup_reply_one.add(item).add(item2).add(item3)

# markup_reply_two = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup_reply_three = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Отменить анализирование дня')
markup_reply_three.add(item)

markup_reply_four = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Да')
item2 = types.KeyboardButton('Нет')
markup_reply_four.add(item).add(item2)


markup_reply_five = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Было')
item2 = types.KeyboardButton('Отменили')
markup_reply_five.add('Отменить анализирование событий')
markup_reply_five.add(item).add(item2)


markup_reply_six = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Отменить добавление календаря')
markup_reply_six.add(item)

markup_reply_seven = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Раз в месяц')
item2 = types.KeyboardButton('Раз в неделю')
item3 = types.KeyboardButton('Отменить изменение дня')
markup_reply_seven.add(item).add(item2)
markup_reply_seven.add(item3)

markup_reply_eight = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Понедельник')
item2 = types.KeyboardButton('Вторник')
item3 = types.KeyboardButton('Среда')
item4 = types.KeyboardButton('Четверг')
item5 = types.KeyboardButton('Пятница')
item6 = types.KeyboardButton('Суббота')
item7 = types.KeyboardButton('Воскресенье')
item8 = types.KeyboardButton('Отменить изменение дня')
markup_reply_eight.add(item8)
markup_reply_eight.add(item).add(item2)
markup_reply_eight.add(item3).add(item4)
markup_reply_eight.add(item5).add(item6)
markup_reply_eight.add(item7)

markup_reply_nine = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Отменить изменение времени')
markup_reply_nine.add(item)


markup_reply_ten = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton('Отменить добавление вопросов')
markup_reply_ten.add(item)


def clear_keyboard():
    return types.ReplyKeyboardMarkup(resize_keyboard=True)