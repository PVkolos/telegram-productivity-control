from create import bot, db
from . import machines
from google_api import table
from matplotlib_my import preparation
from Keyboards.reply import clear_keyboard
from Keyboards.inline import markup_inline_two


async def commands(message):
    if message.text == '/sheets':
        await sheets(message)
    elif message.text == '/my_sheets':
        await my_sheets(message)
    elif message.text == '/settings':
        await settings(message)
    elif message.text == '/analysis':
        await analysis(message)
    elif message.text == '/add_calendar':
        await add_calendar(message)
    elif message.text == '/plans':
        await plans(message)
    elif message.text == '/questions':
        await questions(message)
    elif message.text == '/answer_quests':
        await answer_quests(message)
    elif message.text == '/command_for_admin':
        await preparation(message.from_user.id)
    elif message.text == '/edit_every_day':
        await every_day(message)


async def every_day(message):
    sh = db.get_id_sheets(message.from_user.id)
    if sh:
        await machines.edit_every_day_quests(message)
    else:
        await bot.send_message(message.from_user.id,
                               'Увы, вы не указали гугл таблицу, без этого бот работать не будет. Нажмите /sheets чтобы указать гугл sheets')


async def answer_quests(message):
    sh = db.get_id_sheets(message.from_user.id)
    if sh:
        if db.get_quests(message.from_user.id)[0][0]:
            await machines.start_answer(message)
        else:
            await bot.send_message(message.from_user.id, 'Вы не указали вопросы боту. Нажмите /questions чтобы указать вопросы.')
    else:
        await bot.send_message(message.from_user.id,
                               'Увы, вы не указали гугл таблицу, без этого бот работать не будет. Нажмите /sheets чтобы указать гугл sheets')


async def questions(message):
    sh = db.get_id_sheets(message.from_user.id)
    if sh:
        await machines.quests_start(message)
    else:
        await bot.send_message(message.from_user.id,
                               'Увы, вы не указали гугл таблицу, без этого бот работать не будет. Нажмите /sheets чтобы указать гугл sheets')


async def plans(message):
    name = message.from_user.first_name
    await bot.send_message(message.from_user.id, f'{name}, я рад что вас заинтересовал наш бот и его дальшнейее развитие. \nВ скором будущем планируется несколько обновлений:\n'
                                                 f'1️⃣. Мы планируем добавить систему двадцати одного вопроса. Вы указываете вопросы (количество - пожеланию). В выбранный вами день '
                                                 f'бот будет задавать вам эти вопросы. Бот будет отслеживать динамику ваших ответов.\n2️⃣. Бот будет каждый месяц в конце слать вам '
                                                 f'график основанный на цифрах (из анализа дня). ')


async def add_calendar(message):
    sh = db.get_id_sheets(message.from_user.id)
    if sh:
        await machines.calendar_state(message)
    else:
        await bot.send_message(message.from_user.id, 'Увы, вы не указали гугл таблицу, без этого бот работать не будет. Нажмите /sheets чтобы указать гугл sheets')


async def sheets(message):
    await machines.get_sheets(message)


async def settings(message):
    quest = db.get_time_of_questions(message.from_user.id)
    days = db.get_time_of_day_user(message.from_user.id)
    if type(quest[0][0]) is int:
        await bot.send_message(message.from_user.id,
                               f'Время ежедневной аналитики: <b>{str(days[0][0])[0] + str(days[0][0])[1]}:{str(days[0][0])[2] + str(days[0][0])[3]}</b>\n'
                               f'День ответа на вопросы: <b>{quest[0][0]}-ое число каждого месяца</b>', reply_markup=markup_inline_two)
    else:
        an = quest[0][0]
        if not quest[0][0]:
            an = 'не задано'
        await bot.send_message(message.from_user.id,
                               f'Время ежедневной аналитики: <b>{str(days[0][0])[0] + str(days[0][0])[1]}:{str(days[0][0])[2] + str(days[0][0])[3]}</b>\n'
                               f'День ответа на вопросы: <b>{an}</b>', reply_markup=markup_inline_two)


async def analysis(message):
    sh = db.get_id_sheets(message.from_user.id)
    if sh:
        days = db.get_pass_days(message.from_user.id)
        if not days[0][0]: # Если нет пропущенных дней
            await machines.yn(message)
        elif days:
            markup_reply = clear_keyboard()
            markup_reply.add('Отменить анализирование дня')
            for day in days[0][0].split(','):
                markup_reply.add(day)
            await machines.quest(message, markup_reply)
    else:
        await bot.send_message(message.from_user.id, 'Увы, вы не указали гугл таблицу, без этого бот работать не будет. Нажмите /sheets чтобы указать гугл sheets')


async def my_sheets(message):
    sh = db.get_id_sheets(message.from_user.id)
    if sh:
        tabl = db.get_id_sheets(message.from_user.id)
        if tabl:
            if 'None' not in str(db.get_id_calendar(message.from_user.id)):
                text = f'У вас также задан гугл календарь. Вот его идентификатор доступа - {db.get_id_calendar(message.from_user.id)}. Бот берет оттуда мероприятия для анализа'
            else:
                text = 'У вас не задан гугл календарь. Если хотите анализировать еще и свои мероприятия - задайте календарь командой /add_calendar'
            tbl = await table(db.get_id_sheets(message.from_user.id))
            await bot.send_message(message.from_user.id, f'Ваша гугл таблица называется <b>"{tbl[0]}"</b>\nСсылка - {tbl[1]}\n' + text)
        else:
            await bot.send_message(message.from_user.id, 'Бот еще не создал вам гугл таблицу. Чтобы создать '
                                                         'таблицу введите /sheets')
    else:
        await bot.send_message(message.from_user.id, 'Увы, вы не указали гугл таблицу, без этого бот работать не будет. Нажмите /sheets чтобы указать гугл sheets')
