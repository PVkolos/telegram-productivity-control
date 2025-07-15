import datetime

from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, '../credentials.json')
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


import gspread
import gspread_asyncio


def get_creds():
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


async def create_table(email):
    global agcm
    agc = await agcm.authorize()
    ss = await agc.create("Контроль продуктивности")
    link = "https://docs.google.com/spreadsheets/d/{0}".format(ss.id)
    await agc.insert_permission(ss.id, email, perm_type="user", role="writer")

    ws = await ss.add_worksheet("Дневная продуктивность", 1000, 1000)

    cl = []
    lst = ['Дата']
    for i in range(len(lst)):
        cl.append(gspread.cell.Cell(1, i + 1, lst[i]))
    await ws.update_cells(cl)
    # await ws.batch_update(body)
    return f'Спасибо, ваша таблица была создана и настроена. Теперь вы можете пользоваться ботом ✅\nСсылка на таблицу - {link}\nЕсли вы потеряете ссылку,' \
           f'то введите команду /my_sheets и бот вам вышлет ссылку.\nНапоминание⚠️\nЕсли желаете, добавьте свой календарь командой /add_calendar\n' \
               'Каждый день в ваше время (по умолчанию 21:00) бот будет вам присылать напоминание о том, что нужно проанализировать ваш день. Если в календаре на этот день были запланированы ' \
               'мероприятия, бот предложит вам их проанализировать. '


async def create_sheet_calendar(spreadsheet_id):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        try:
            ws = await ss.add_worksheet("Мероприятия. Анализ", 1000, 1000)
        except Exception as e:
            if 'already exists' in str(e):
                ws = await ss.worksheet("Мероприятия. Анализ")
        cl = []
        lst = ['Дата', 'Название мероприятия', 'Эффективность', 'Продолжительность']
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(1, i + 1, lst[i]))
        await ws.update_cells(cl)
        return "Я создал дополнительный лист на вашей гугл таблице. На этом листе я буду записывать анализ ваших мероприятий."
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def create_sheet_questions(spreadsheet_id, quets):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        try:
            ws = await ss.add_worksheet("Самоанализ по вопросам", 1000, 1000)
        except Exception as e:
            if 'already exists' in str(e):
                ws = await ss.worksheet("Самоанализ по вопросам")
            else:
                return f'Error_1293: Сообщите разработчику. Error Text: {str(e)}'
        cl = []
        ln = await ws.get_all_values()
        lst = ['Дата'] + quets
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(len(ln) + 2, i + 1, lst[i]))
        await ws.update_cells(cl)
        await ws.format(f'A{len(ln) + 2}:{chr(66 + len(lst))}{len(ln) + 2}', {'textFormat': {'bold': True}})
        return "Я создал дополнительный лист на вашей гугл таблице. На этом листе я буду записывать ваши вопросы и ответы"
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def table(spreadsheet_id):
    global agcm
    agc = await agcm.authorize()
    ss = await agc.open_by_key(spreadsheet_id)
    return ss.title, "https://docs.google.com/spreadsheets/d/{0}".format(ss.id)


async def set_event_analysis(date, event, efficiency, how_time, spreadsheet_id):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        ws = await ss.worksheet("Мероприятия. Анализ")
        lst = [date, event, efficiency, how_time]
        ln = await ws.get_all_values()
        cl = []
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(len(ln) + 1, i + 1, lst[i]))
        await ws.update_cells(cl)
        return 'Анализ мероприятия прошел успешно. Мы записали в таблицу ваши сведения✅'
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def set_day_analysis(day, int_emot, str_emot, int_phys, str_phys, spreadsheet_id):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        ws = await ss.worksheet("Дневная продуктивность")
        lst = [day, int_emot, str_emot, int_phys, str_phys]
        ln = await ws.get_all_values()
        cl = []
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(len(ln) + 1, i + 1, lst[i]))
        await ws.update_cells(cl)
        return 'Анализ дня прошел успешно. Мы записали в таблицу ваши сведения✅'
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def set_answer(spreadsheet_id, data, lst):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        ws = await ss.worksheet("Самоанализ по вопросам")
        ln = await ws.get_all_values()
        lst = [data, *lst]
        cl = []
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(len(ln) + 1, i + 1, lst[i]))
        await ws.update_cells(cl)
        return 'Успешно. Мы записали в таблицу ваши ответы✅'
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def edit_everyday_quests(spreadsheet_id, lst):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        ws = await ss.worksheet("Дневная продуктивность")
        ln = await ws.get_all_values()
        lst = [*lst]
        cl = []
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(len(ln) + 2, i + 2, lst[i].upper()))
        await ws.update_cells(cl)
        await ws.format(f'B{len(ln) + 2}:{chr(66 + len(lst))}{len(ln) + 2}', {'textFormat': {'bold': True}})
        return 'Успешно. Мы записали в таблицу ваши новые вопросы✅'
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def everyday_answer(spreadsheet_id, date, lst):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)
        ws = await ss.worksheet("Дневная продуктивность")
        ln = await ws.get_all_values()
        lst = [date, *lst]
        cl = []
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(len(ln) + 1, i + 1, lst[i]))
        await ws.update_cells(cl)
        return 'Успешно. Мы записали в таблицу ваши ответы✅'
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'
        return str(e)


async def read(SAMPLE_SPREADSHEET_ID, name_sheet='Дневная продуктивность',):
    global agcm
    agc = await agcm.authorize()
    ss = await agc.open_by_key(SAMPLE_SPREADSHEET_ID)
    ws = await ss.worksheet(name_sheet)
    ln = await ws.get_all_values()
    return ln


async def add_sheet(spreadsheet_id):
    global agcm
    agc = await agcm.authorize()
    try:
        ss = await agc.open_by_key(spreadsheet_id)

        try:
            ws = await ss.add_worksheet("Дневная продуктивность", 1000, 1000)
        except: ws = await ss.worksheet("Дневная продуктивность")

        cl = []
        lst = ['Дата', '(ваши вопросы будут ниже)']
        for i in range(len(lst)):
            cl.append(gspread.cell.Cell(1, i + 1, lst[i]))
        await ws.update_cells(cl)
        return 'Спасибо. Мы успешно создали необходимые листы в вашей таблице. Теперь вы можете пользоваться ботом.\nНапоминание⚠️\nЕсли желаете, добавьте свой календарь командой /add_calendar\n' \
               'Каждый день в ваше время (по умолчанию 21:00) бот будет вам присылать напоминание о том, что нужно проанализировать ваш день. Если в календаре на этот день были запланированы ' \
               'мероприятия, бот предложит вам их проанализировать. '
    except Exception as e:
        if 'not have permission' in str(e):
            return 'Вы не предоставили доступ к таблице нашему боту. ' \
                   'Предоставьте доступ к вашей таблице этому аккаунту:\n' \
                   '<u>account-519@oooo-359817.iam.gserviceaccount.com</u>'

