import asyncio
from create import bot, db
import datetime
from google_api import read
# from matplotlib_my import preparation
from GLOBAL import WEEK
from dateutil.parser import parse


async def check_time():
    while True:
        await asyncio.sleep(60)
        await intermediary()


def is_valid_date(date_string):
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


async def intermediary():
    times = db.get_time_of_day()
    now = datetime.datetime.now()
    minute = str(now.minute)
    hour = str(now.hour)
    if len(str(now.minute)) == 1:
        minute = '0' + str(now.minute)
    if len(str(now.hour)) == 1:
        hour = '0' + str(hour)
    for time in times:
        if str(time[0]) == hour + minute:
            try:
                # if now.day == 31:
                #     await preparation(time[1])

                time_quest = db.get_time_of_questions(time[1])[0][0]
                if time_quest is not None:
                    if str(time_quest).isdigit() and int(time_quest) == now.day:
                        await bot.send_message(time[1], 'Сегодня день для ответов на вопросы. Нажмите на /answer_quests для того, чтобы ответить на вопросы.')
                    elif WEEK[datetime.datetime.weekday(now)] == time_quest:
                        await bot.send_message(time[1], 'Сегодня день для ответов на вопросы. Нажмите на /answer_quests для того, чтобы ответить на вопросы.')

                if db.get_id_sheets(time[1]):
                    ans = await read(db.get_id_sheets(time[1]))
                    if ((not ans[-1][0] == str(datetime.date.today() - datetime.timedelta(days=1))) and
                        (not ans[-1][0] == str(datetime.date.today()))) and is_valid_date(ans[-1][0]):
                        days = db.get_pass_days(time[1])
                        if days[0][0]:
                            days = days[0][0]
                        else:
                            days = ''
                        if len(days.split(',')) >= 4:
                            days = ','.join(days.split(',')[1:])

                        days += f"{str(datetime.date.today() - datetime.timedelta(days=1))},"
                        db.update_info(time[1], 'passs', days)
                    await bot.send_message(time[1], 'НАСТАЛО время подводить итоги дня! '
                                                    'Проанализируем ваш день. Для этого нажмите на команду /analysis')
                else:
                    await bot.send_message(time[1], 'Время анализа дня, но у вас не задана гугл таблица. Введите /sheets')
            except Exception as e:
                print('Error analysis_1: ', str(e))
