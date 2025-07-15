import copy
import datetime

from create import bot, db
from aiogram import types
from States.users import Get_Sheets, Analysis, Days, Get_calendar, Analysis_events, Event, Quests, Time_analysis, Time_quests, Answer, Answer_Every_Day, Edit_quests_every_day
from Keyboards.reply import markup_reply_one, markup_reply_three, clear_keyboard, markup_reply_five, markup_reply_six, markup_reply_seven, markup_reply_eight, markup_reply_nine, markup_reply_ten
from Keyboards.inline import markup_inline_one
from Errors.errors import EmailError
from google_api import create_table, add_sheet, set_day_analysis, read, create_sheet_calendar, set_event_analysis, create_sheet_questions, set_answer, everyday_answer, edit_everyday_quests
from calendar_api import add_calendar, get_events
from dateutil.parser import parse


dct = dict()


async def edit_every_day_quests(message):
    await bot.send_message(message.from_user.id, 'Вы решили изменить свои ежедневные вопросы.\n<b>Перечислите вопросы в одном сообщении, КАЖДЫЙ С НОВОЙ СТРОКИ!</b>', reply_markup=markup_reply_ten)
    await Edit_quests_every_day.quests_edit.set()


async def quests_edit(message, state):
    try:
        await state.finish()
        qsts = message.text.split('\n')
        db.update_info(message.from_user.id, 'everyday', '砺'.join(qsts))
        ans = await edit_everyday_quests(db.get_id_sheets(message.from_user.id), qsts)
        await bot.send_message(message.from_user.id, ans, reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await bot.send_message(message.from_user.id, 'Временная ошибка. Немного подождите....')
        await bot.send_message(1229555610, f'G-Error: {str(e)}')


async def start_answer(message):
    try:
        quests_user = db.get_quests(message.from_user.id)[0][0]
        dct[message.from_user.id] = []
        text_sms = quests_user.split('.=.')[len(dct[message.from_user.id])]
        await bot.send_message(message.from_user.id, text_sms,  reply_markup=markup_reply_ten)
        await Answer.answer.set()
    except Exception as e:
        await bot.send_message(message.from_user.id, 'Временна ошибка. Немного подождите....')
        await bot.send_message(1229555610, f'F-Error: {str(e)}')


async def answer(message, state):
    dct[message.from_user.id].append(message.text)
    quests_user = db.get_quests(message.from_user.id)[0][0]
    if len(dct[message.from_user.id]) == len(quests_user.split('.=.')):
        ans = await set_answer(db.get_id_sheets(message.from_user.id), str(datetime.date.today()), dct[message.from_user.id])
        dct[message.from_user.id] = None
        await bot.send_message(message.from_user.id, ans, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, quests_user.split('.=.')[len(dct[message.from_user.id])])


async def change_time_quests(message):
    await bot.send_message(message.from_user.id, 'Вы хотели бы отвечать на вопросы раз в месяц или раз в неделю?',
                           reply_markup=markup_reply_seven)
    await Time_quests.one_stage.set()


async def one_stage(message, state):
    if message.text == 'Раз в месяц':
        await bot.send_message(message.from_user.id,
                               'Введите цифру от 1 до 28 (день месяца в который бот будет слать напоминание о вопросах)')
        await Time_quests.next()
    elif message.text == 'Раз в неделю':
        await bot.send_message(message.from_user.id,
                               'Выберите из списка (день недели в который бот будет слать напоминание о вопросах)',
                               reply_markup=markup_reply_eight)
        await Time_quests.next()
    else:
        await bot.send_message(message.from_user.id, 'Нажмите на одну из кнопок выше!')


async def time_quests(message, state):
    if message.text.isdigit() and 1 <= int(message.text) < 29:
        await bot.send_message(message.from_user.id,
                               f'Отлично. {message.text}-го числа каждого месяца бот будет слать вам напоминание о том, что вам необходимо ответить на ваши вопросы!',
                               reply_markup=types.ReplyKeyboardRemove())
        db.update_info(message.from_user.id, 'time_of_quest', message.text)
        await state.finish()
    elif message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
        await bot.send_message(message.from_user.id,
                               f'Отлично. В каждый {message.text} бот будет слать вам напоминание о том, что вам необходимо ответить на ваши вопросы!',
                               reply_markup=types.ReplyKeyboardRemove())
        db.update_info(message.from_user.id, 'time_of_quest', message.text)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Введите верное значение')


async def change_time_if_day(message):
    await bot.send_message(message.from_user.id, 'Ниже введите время в 24-ёх часовом формате. Часы и минуты. (Пример:\n21-00)', reply_markup=markup_reply_nine)
    await Time_analysis.time_analysis.set()


async def time_analysis(message, state):
    if '-' in message.text and len(message.text) == 5 and message.text[0:2].isdigit() and message.text[3:5].isdigit() and int(message.text[0:2]) < 24 and int(message.text[3:5]) < 60:
        await bot.send_message(message.from_user.id, 'Новое время анализа дня было добавлено', reply_markup=types.ReplyKeyboardRemove())
        db.update_info(message.from_user.id, 'time_of_day', f'{message.text[0:2]}{message.text[3:5]}')
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Вы неверно ввели время. Введите в подобном формате (21-00)')


async def quests_start(message):
    await bot.send_message(message.from_user.id,
                           'Вы решили дать боту свои вопросы. Введите их всех в <b>одном сообщении, каждый вопрос на новой строке</b>.',
                           reply_markup=markup_reply_ten)
    await Quests.quests.set()


async def quests(message, state):
    quests_lst = message.text.split('\n')
    db.update_info(message.from_user.id, 'quest', '.=.'.join(quests_lst))
    await bot.send_message(message.from_user.id,
                           'Хорошо, мы записали ваши вопросы. Сейчас бот создаст необходимый лист на вашей гугл таблице, на который будут записываться ваши ответы.',
                           reply_markup=types.ReplyKeyboardRemove())
    ans = await create_sheet_questions(db.get_id_sheets(message.from_user.id), quests_lst)
    if 'создал' in ans:
        await bot.send_message(message.from_user.id, 'Бот создал лист на вашей таблице. Чтобы настроить время отправки вам уведомления о ваших вопросах нажмите /settings\n'
                                                     '(БЕЗ ЭТОГО БОТ НЕ БУДЕТ ВАМ СЛАТЬ НАПОМИНАНИЕ О ВОПРОСАХ)')
    else:
        await bot.send_message(message.from_user.id, 'Произошла ошибка:', ans)
        print(111151, ans)
    await state.finish()


async def stop_analysis_events(message, state):
    await state.finish()
    flag = db.get_flag(message.from_user.id)
    if flag.split("_")[0] == 'True':
        if int(flag.split("_")[1]) > 0:
            await bot.send_message(message.from_user.id,
                                   'Вы проанализировали не все дни из списка. '
                                   'Нажмите на /analysis, чтобы продолжить анализировать')
        else:
            await bot.send_message(message.from_user.id,
                                   'Вы рассчитались со всеми долгами. Чтобы проанализировать '
                                   'СЕГОНДЯШНИЙ день, нажмите /analysis')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы проанализировали все дни. До встречи завтра.👋')


async def check_events_and_days(message, day, event):
    events = db.get_events(message.from_user.id)[0][0].split(',')
    events.remove(event)
    db.update_info(message.from_user.id, 'events', ','.join(events))
    if not len(events):
        flag = db.get_flag(message.from_user.id)
        if flag.split("_")[0] == 'True':
            if int(flag.split("_")[1]) > 0:
                await bot.send_message(message.from_user.id, f'Вы проанализировали все мероприятия {day}, но Вы проанализировали не все дни из списка. '
                                                             'Нажмите на /analysis, чтобы продолжить анализировать', reply_markup=types.ReplyKeyboardRemove())
            else:
                await bot.send_message(message.from_user.id, f'Вы проанализировали все мероприятия {day} и Вы рассчитались со всеми долгами. Чтобы проанализировать '
                                                             'СЕГОНДЯШНИЙ день, нажмите /analysis', reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(message.from_user.id, 'Вы проанализировали все мероприятия и все дни. До встречи завтра.👋', reply_markup=types.ReplyKeyboardRemove())
    else:
        markup = clear_keyboard()
        markup.add('Отменить анализирование событий')
        for ev in events:
            markup.add(ev)
        await Event.event.set()
        await bot.send_message(message.from_user.id, f'Вы проанализировали <b>"{event}"</b>, но у вас остались еще мероприятия для анализа. Выберите из списка', reply_markup=markup)


async def analysis_events(tg_id, day, events):
    markup = clear_keyboard()
    markup.add('Отменить анализирование событий')
    for event in events[0][0].split(','):
        markup.add(event)
    await bot.send_message(tg_id, f'Выберите мероприятие, которое хотите проанализировать. {day} '
                                  f'у вас были такие мероприятия:', reply_markup=markup)
    await Event.event.set()


async def event(message, state):
    events = db.get_events(message.from_user.id)[0][0].split(',')
    if message.text not in events:
        await bot.send_message(message.from_user.id, 'Нажмите на любое мероприятие ИЗ предоставленного списка!!!!')
    else:
        await state.finish()
        await Analysis_events.was.set()
        async with state.proxy() as data:
            data['events'] = events
            data['event'] = message.text
            await bot.send_message(message.from_user.id, f'Ответьте на пару вопросов.\n1️⃣. Мероприятие <b>"{data["event"]}"</b> было?', reply_markup=markup_reply_five)


async def was(message, state):
    if message.text == 'Отменили':
        async with state.proxy() as data:
            event_ = data['event']
            await state.finish()
        await check_events_and_days(message, db.get_temporary(message.from_user.id), event_)
    elif message.text == 'Было':
        await bot.send_message(message.from_user.id,
                               '2️⃣. Отлично, оцените эффективность встречи от 1 до 10. (0 - мероприятие прошло крайне '
                               'не продуктивно, 10 - решили все поставленные задачи и даже больше того.)', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отменить анализирование событий'))
        await Analysis_events.next()
    else:
        await bot.send_message(message.from_user.id, 'Выберите вариант из предложенного списка.')


async def efficiency(message, state):
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        async with state.proxy() as data:
            data['efficiency'] = message.text
            await bot.send_message(message.from_user.id, '3️⃣. Хорошо! Как долго длилось ваше мероприятие?')
            await Analysis_events.next()
    else:
        await bot.send_message(message.from_user.id, 'Введите <b>число от 1 до 10</b>')


async def how_time(message, state):
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id, f'Мероприятие с такими показателями:\nНазвание: {data["event"]}'
                                                     f'\nЭффективность: {data["efficiency"]}\n'
                                                     f'Продолжительность: {message.text}\nбудет добавлено к вам в гугл таблицу', reply_markup=types.ReplyKeyboardRemove())
        result = await set_event_analysis(db.get_temporary(message.from_user.id), data["event"], data["efficiency"], message.text, db.get_id_sheets(message.from_user.id))
        await bot.send_message(message.from_user.id, result)
        event_ = data['event']
        await state.finish()
    await check_events_and_days(message, db.get_temporary(message.from_user.id), event_)


async def quest(message, markup_reply):
    await Days.value_of_day.set()
    await bot.send_message(message.from_user.id, 'Пришло время заполнить анализ сегодняшнего дня. Только вот вы не заполняли анализ '
                               'несколько дней. Выберите какой день хотите заполнить сейчас. К сожалению, сегодняшний '
                               'день вы не сможете заполнить, пропустив предыдущие!',
                           reply_markup=markup_reply)


async def value_of_day(message, state):
    async with state.proxy() as data:
        data['days'] = db.get_pass_days(message.from_user.id)[0][0].split(',')
        if message.text not in data['days']:
            await bot.send_message(message.from_user.id, 'Нажмите на любой день ИЗ предоставленного списка!!!!')
        else:
            data['day'] = message.text
            await state.finish()
            await yn(message, data['day'])


async def yn(message, day=None):
    try:
        if db.get_every_day_quests_user(message.from_user.id)[0][0]:
            ans = await read(db.get_id_sheets(message.from_user.id))
            if not day: d = str(datetime.date.today())
            if day: d = copy.deepcopy(day)
            if not ans[-1][0] == d:
                dct[message.from_user.id] = day
                qsts = db.get_every_day_quests_user(message.from_user.id)[0][0]
                dct[f'{message.from_user.id}_'] = []
                await Answer_Every_Day.answer_every_day.set()
                await bot.send_message(message.from_user.id, qsts.split('砺')[0], reply_markup=markup_reply_three)
            else:
                await bot.send_message(message.from_user.id, f'Вы уже анализировали день, дважды сделать '
                                                             'этого нельзя❗️', reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(message.from_user.id, 'Вы не задали ежедневные вопросы. Сделайте это командой /edit_every_day')
    except Exception as e:
        await bot.send_message(message.from_user.id, 'Временна ошибка. Немного подождите....')
        await bot.send_message(1229555610, f'M-Error: {str(e)}')


async def answer_every_day(message, state):
    try:
        dct[f'{message.from_user.id}_'].append(message.text)
        qsts = db.get_every_day_quests_user(message.from_user.id)[0][0]
        if len(dct[f'{message.from_user.id}_']) == len(qsts.split('砺')):
            await state.finish()
            await end_analysis(message)
        else:
            await bot.send_message(message.from_user.id, qsts.split('砺')[len(dct[f'{message.from_user.id}_'])],
                                   reply_markup=markup_reply_three)
    except Exception as e:
        await bot.send_message(message.from_user.id, 'Временна ошибка. Немного подождите....')
        await bot.send_message(1229555610, f'P-Error: {str(e)}')


async def end_analysis(message):
    try:
        flag = False
        days = []
        spr = db.get_id_sheets(message.from_user.id)
        if not dct[message.from_user.id]: # Если был анализирован сегодняшний день
            dct[message.from_user.id] = str(datetime.date.today())
        else: # Если был анализирован предыдущий день
            flag = True
            days = db.get_pass_days(message.from_user.id)
            days = days[0][0].split(',')
            days.remove(dct[message.from_user.id])
            days = ','.join(days)
            db.update_info(message.from_user.id, 'passs', days)
        ans = await everyday_answer(spr, dct[message.from_user.id], dct[f'{message.from_user.id}_'])
        await bot.send_message(message.from_user.id, ans, reply_markup=types.ReplyKeyboardRemove())
        events = get_events(db.get_id_calendar(message.from_user.id), dct[message.from_user.id])
        if events:
            db.update_info(message.from_user.id, 'flag', f'{str(flag)}_{len(days)}')
            db.update_info(message.from_user.id, 'events', ','.join(events))
            db.update_info(message.from_user.id, 'temporary', dct[message.from_user.id])
            await bot.send_message(message.from_user.id, f'Хотите проанализировать мероприятия дня {dct[message.from_user.id]}?', reply_markup=markup_inline_one)
        else: # Если нет событий
            if flag: # Если был анализирован НЕ сегодняшний день
                if days: # Если еще остались дни после удаления
                    await bot.send_message(message.from_user.id, 'Вы проанализировали не все дни из списка. '
                                                                 'Нажмите на /analysis, чтобы продолжить анализировать')
                else:
                    await bot.send_message(message.from_user.id, 'Вы рассчитались со всеми долгами. Чтобы проанализировать '
                                                             'СЕГОНДЯШНИЙ день, нажмите /analysis')
    except Exception as e:
        await bot.send_message(message.from_user.id,
                               '❌ Вы написали не совсем так, как нужно. Прочитайте сообщение выше, '
                               'где мы все рассказываем и показываем, и попробуйте снова или обратитесь за помощью к @it_pavel_it',
                               reply_markup=markup_reply_three)
        await bot.send_message(1229555610, f'L-Error: {str(e)}')


async def get_sheets(message):
    await bot.send_message(message.from_user.id, 'Вы хотите использовать свою таблицу или создадим новую?',
                            reply_markup=markup_reply_one)
    await Get_Sheets.your.set()


async def your(message, state):
    async with state.proxy() as data:
        data['variant'] = message.text
    if message.text == 'Моя таблица':
        await bot.send_message(message.from_user.id, 'Хорошо. Раз у вас есть своя таблица - дайте ее мне. '
                                                     'Скиньте ссылку на свою таблицу в сообщении ниже.\n'
                                                     '❗️Обязательно!❗️Сначала дайте разрешение на редактирование вашей таблицы '
                                                     'боту, а потом - скидывайте ссылку. Почта бота - <u>account-519@oooo-359817.iam.gserviceaccount.com</u>')
        await Get_Sheets.next()
    elif message.text == 'Создать новую':
        await bot.send_message(message.from_user.id, 'Замечательно. Для добавления гугл таблицы введите вашу почту.\n'
                                                     '❗️Обязательно!❗️\nВаша почта должна принадлежать Google, то есть оканчиваться'
                                                     ' на @gmail.com\nПожалуйста, указывайте реальную почту, иначе вы не '
                                                     'получите доступа к таблице с данными.',
                               reply_markup=markup_reply_one)
        await Get_Sheets.next()
    else:
        await bot.send_message(message.from_user.id, 'Выберите вариант из предоставленного списка. '
                                                      'Если попали в это меню случайно, то нажмите '
                                                      '"Отменить добавление таблицы"')


async def link(message, state):
    async with state.proxy() as data:
        try:
            if data['variant'] == 'Отменить добавление таблицы':
                await bot.send_message(message.from_user.id, 'Хорошо. Вы всегда сможете добавить гугл таблицу командой '
                                                             '/sheets',
                                       reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
                return
            elif data['variant'] == 'Создать новую':
                email = message.text
                if '@gmail.com' not in email:
                    raise EmailError
                await bot.send_message(message.from_user.id,
                                       'Отлично, дайте ботy несколько секунд для создания и обработки таблицы ⏳')
                result = await create_table(email)
                if 'спасибо' in result.lower():
                    sh = result.split('таблицу - ')[1].split('/d/')[1].split('\n')[0]
                    db.update_info(message.from_user.id, 'sheets', sh)
                    await bot.send_message(message.from_user.id, result,
                                           reply_markup=types.ReplyKeyboardRemove())
                    await state.finish()
                else:
                    await bot.send_message(message.from_user.id, result)
            elif data['variant'] == 'Моя таблица':
                res = await add_sheet(message.text.split('/d/')[1].split('/edit')[0])
                if 'Спасибо' in res: db.update_info(message.from_user.id, 'sheets', message.text.split('/d/')[1].split('/edit')[0])
                await bot.send_message(message.from_user.id, res)
                await state.finish()
        except (EmailError, IndexError):
            await bot.send_message(
                message.from_user.id,
                '❗️Вы ввели неверную почту.❗️\ndurov@gmail.com\n'
                'Пример почты, которую нужно скинуть', reply_markup=markup_reply_one)


async def calendar_state(message):
    await bot.send_message(message.from_user.id, 'Вы собираетесь подключить гугл календарь. Перед этим вам надо сделать '
                                                 'несколько важных шагов.\n1️⃣. В настройках вашего календаря предоставьте доступ боту. Необходимо предоставить доступ уровня 2. (Доступ ко всем сведениям о мероприятиях)'
                                                 '. Этой почте - friends-project@friends-project-359817.iam.gserviceaccount.com\n'
                                                 '2️⃣. В настройках вашего календаря (в самом низу) найдите поле <b>Интеграция календаря</b> и скоприруйте <b>Идентификатор календаря</b>\n'
                                                 '3️⃣. Отправьте боту скопированный вами идентификатор. ', reply_markup=markup_reply_six)
    await Get_calendar.id_calendar.set()


async def id_calendar(message, state):
    result = add_calendar(message.text)
    if 'спасибо' in result.lower():
        await state.finish()
        db.update_info(message.from_user.id, 'calendar', message.text)
        result = await create_sheet_calendar(db.get_id_sheets(message.from_user.id))
        if 'создал' in result.lower():
            await bot.send_message(message.from_user.id, 'Спасибо, мы добавили ваш календарь\n' + result, reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(message.from_user.id, 'Произошла неизвестная ошибка, попробуйте позже')
    else:
        await bot.send_message(message.from_user.id, result)