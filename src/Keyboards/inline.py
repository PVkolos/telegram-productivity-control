from aiogram import types

markup_inline_one = types.InlineKeyboardMarkup()
but1 = types.InlineKeyboardButton(text='Проанализировать', callback_data='tr-yes')
but2 = types.InlineKeyboardButton(text='Отмена', callback_data='tr-no')
markup_inline_one.add(but1)
markup_inline_one.add(but2)


markup_inline_two = types.InlineKeyboardMarkup()
but1 = types.InlineKeyboardButton(text='Изменить время ежедневной аналитики', callback_data='time-analysi')
but2 = types.InlineKeyboardButton(text='Изменить день ответа на вопросы', callback_data='time-day')
markup_inline_two.add(but1)
markup_inline_two.add(but2)