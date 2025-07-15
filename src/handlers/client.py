from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create import bot, db
from . import commands
from States.users import Get_Sheets, Analysis, Days, Get_calendar, Analysis_events, Event, Quests, Time_analysis, Time_quests, Answer, Answer_Every_Day, Edit_quests_every_day
from . import machines


async def user_registration(message):
    if not db.check_user_on_db(message.from_user.id):
        db.add_users_to_db(message.from_user.id, message.from_user.username)

    await get_help(message)
    if not db.get_id_sheets(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Укажите вашу гугл таблицу. Без этого, увы, '
                                                     'бот работать не будет.\nВведите команду /sheets для добавления таблицы.')


async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 's':
        await state.finish()
        await callback_query.message.delete()
        temporary = db.get_temporary(callback_query.from_user.id)
        events = db.get_events(callback_query.from_user.id)
        await machines.analysis_events(callback_query.from_user.id, temporary, events)
    if code == 'o':
        await machines.stop_analysis_events(callback_query, state)
        await callback_query.message.delete()
    if code == 'i':
        await machines.change_time_if_day(callback_query)
    if code == 'y':
        await machines.change_time_quests(callback_query)


async def get_help(message):
    name = message.from_user.first_name
    text = f'Приветствую, {name}. Раз вы запустили этого бота, значит вы хотите начать следить за своей продуктивностью, хотите отслеживать прогресс/регресс в любых сферах вашей жизни,' \
           ' вы хотите отслеживать эффективность и качество ваших встреч и мероприятий. В общем и целом - бот поможет вам ' \
           'контролировать ваше время. Теперь вы не будете терять его понапрасну.\n\n' \
            'Функционал бота:\n' \
            '1. Каждый день в 21:00 (время меняется в настройках командой /settings) бот будет предлагать вам проанализировать сегодняшний день. Важно! Задайте боту свои ежедневные вопросы сразу же, как будет возможность, чтобы работа происходила корректно! /edit_every_day\n' \
           '2. Если вы подключили гугл календарь, то после анализа каждого дня бот будет предлагать вам проанализировать ваши мероприятия сегодняшнего дня, после анализа самого дня.\n' \
           '3. По желанию, вы можете задать некий список вопросов боту, которые, раз в неделю (этот показатель тоже настраивается /settings), будут предлагаться вам для ответа. Так вы сможете отслеживать динамику ваших ответов.' \
           ' Чтобы задать вопросы введите команду /questions' \
           '\nИзменить любые настройки бота можно введя команду /settings\n'
    await bot.send_message(message.from_user.id, text)


async def stop_state(message, state):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Хорошо, спасибо.',
                           reply_markup=types.ReplyKeyboardRemove())


# async def mn(message):
#     r = sr.Recognizer()
#
#     file_id = message.voice.file_id
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     await bot.download_file(file_path, "123.wav")
#     harvard = sr.WavFile('E:\\Profile\\Desktop\\Проекты\\Python\\Productivity control\\src\\123.wav')
#     query = r.recognize_google(harvard, language='ru-RU')
#     print(111, query)
#     # with harvard as source:
#     #     audio = r.record(source)
#     #     print(type(audio))
#     #     query = r.recognize_google(audio, language='ru-RU')
#     #     print(111, query)
#     # os.remove('../123.mp3')


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(user_registration, commands=['start', 'run'])
    dp.register_message_handler(commands.commands, commands=['sheets'])
    dp.register_message_handler(commands.commands, commands=['my_sheets'])
    dp.register_message_handler(commands.commands, commands=['settings'])
    dp.register_message_handler(commands.commands, commands=['analysis'])
    dp.register_message_handler(commands.commands, commands=['add_calendar'])
    dp.register_message_handler(commands.commands, commands=['plans'])
    dp.register_message_handler(commands.commands, commands=['questions'])
    dp.register_message_handler(commands.commands, commands=['answer_quests'])
    dp.register_message_handler(commands.commands, commands=['command_for_admin'])
    dp.register_message_handler(commands.commands, commands=['edit_every_day'])
    dp.register_message_handler(get_help, commands=['help'])
    dp.register_message_handler(stop_state, Text(equals='Отменить добавление таблицы'), state="*")
    dp.register_message_handler(stop_state, Text(equals='Отменить анализирование дня'), state="*")
    dp.register_message_handler(stop_state, Text(equals='Отменить добавление календаря'), state="*")
    dp.register_message_handler(stop_state, Text(equals='Отменить изменение дня'), state="*")
    dp.register_message_handler(stop_state, Text(equals='Отменить изменение времени'), state="*")
    dp.register_message_handler(stop_state, Text(equals='Отменить добавление вопросов'), state="*")
    dp.register_message_handler(machines.stop_analysis_events, Text(equals='Отменить анализирование событий'), state="*")
    dp.register_callback_query_handler(process_callback)
    dp.register_message_handler(machines.your, state=Get_Sheets.your)
    dp.register_message_handler(machines.link, state=Get_Sheets.link)
    dp.register_message_handler(machines.value_of_day, state=Days.value_of_day)
    dp.register_message_handler(machines.id_calendar, state=Get_calendar.id_calendar)
    dp.register_message_handler(machines.event, state=Event.event)
    dp.register_message_handler(machines.was, state=Analysis_events.was)
    dp.register_message_handler(machines.efficiency, state=Analysis_events.efficiency)
    dp.register_message_handler(machines.how_time, state=Analysis_events.how_time)
    dp.register_message_handler(machines.quests, state=Quests.quests)
    dp.register_message_handler(machines.time_analysis, state=Time_analysis.time_analysis)
    dp.register_message_handler(machines.one_stage, state=Time_quests.one_stage)
    dp.register_message_handler(machines.time_quests, state=Time_quests.time_quests)
    dp.register_message_handler(machines.answer, state=Answer.answer)
    dp.register_message_handler(machines.answer_every_day, state=Answer_Every_Day.answer_every_day)
    dp.register_message_handler(machines.quests_edit, state=Edit_quests_every_day.quests_edit)
    # dp.register_message_handler(mn, content_types=types.ContentType.VOICE)
