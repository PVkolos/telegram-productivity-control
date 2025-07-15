from aiogram.dispatcher.filters.state import StatesGroup, State


class Get_Sheets(StatesGroup):
    your = State()
    link = State()


class Days(StatesGroup):
    value_of_day = State()


class Analysis(StatesGroup):
    st1 = State()
    emotional = State()
    phys = State()


class Get_calendar(StatesGroup):
    id_calendar = State()


class Analysis_events(StatesGroup):
    was = State()
    efficiency = State()
    how_time = State()


class Event(StatesGroup):
    event = State()


class Quests(StatesGroup):
    quests = State()


class Time_analysis(StatesGroup):
    time_analysis = State()


class Time_quests(StatesGroup):
    one_stage = State()
    time_quests = State()


class Answer(StatesGroup):
    answer = State()


class Answer_Every_Day(StatesGroup):
    answer_every_day = State()


class Edit_quests_every_day(StatesGroup):
    quests_edit = State()
