import sqlite3
import os.path


class DataBase:
    def __init__(self, db_name="user.db"):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, db_name)
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    """Проверка на наличие пользователя в бд"""
    def check_user_on_db(self, id):
        with self.connection:
            result = self.cursor.execute("select id from users where tg_id = ?", (id,)).fetchall()
            return bool(len(result))

    """Добавление пользователя в бд"""
    def add_users_to_db(self, id, username):
        with self.connection:
            self.cursor.execute("insert into users (tg_id, username) values (?, ?)", (id, username,)).fetchall()
            self.connection.commit()

    """Получение id гугл таблицы пользователя"""
    def get_id_sheets(self, tg_id):
        with self.connection:
            link = self.cursor.execute(f"select sheets from users where tg_id = ?", (tg_id,)).fetchall()
            return link[0][0]

    """Изменение информации о пользователе"""
    def update_info(self, tg_id, what, new):
        with self.connection:
            self.cursor.execute(f"update users set {what} = ? where tg_id = ?", (new, tg_id,)).fetchall()

    """Получение времени дневной аналитики пользователей"""
    def get_time_of_day(self):
        with self.connection:
            time = self.cursor.execute(f"select time_of_day, tg_id from users").fetchall()
            return time

    """Получение пропущенных дней аналитики пользователя"""
    def get_pass_days(self, tg_id):
        with self.connection:
            days = self.cursor.execute(f"select passs from users where  tg_id = ?", (tg_id,)).fetchall()
            return days

    """Получение id гугл календаря пользователя"""
    def get_id_calendar(self, tg_id):
        with self.connection:
            link = self.cursor.execute(f"select calendar from users where tg_id = ?", (tg_id,)).fetchall()
            return link[0][0]

    """Получение временной переменной пользователя"""
    def get_temporary(self, tg_id):
        with self.connection:
            temporary = self.cursor.execute(f"select temporary from users where tg_id = ?", (tg_id,)).fetchall()
            return temporary[0][0]

    """Получение мероприятий пользователя"""
    def get_events(self, tg_id):
        with self.connection:
            events = self.cursor.execute(f"select events from users where tg_id = ?", (tg_id,)).fetchall()
            return events

    """Получение flag пользователя"""
    def get_flag(self, tg_id):
        with self.connection:
            flag = self.cursor.execute(f"select flag from users where tg_id = ?", (tg_id,)).fetchall()
            return flag[0][0]

    """Получение вопросов пользователя"""
    def get_quests(self, tg_id):
        with self.connection:
            quests = self.cursor.execute(f"select quest from users where tg_id = ?", (tg_id,)).fetchall()
            return quests

    """Получение времени дневной аналитики пользователей"""
    def get_time_of_questions(self, tg_id):
        with self.connection:
            time = self.cursor.execute(f"select time_of_quest from users where tg_id = ?", (tg_id,)).fetchall()
            return time

    """Получение времени дневной аналитики пользователя"""
    def get_time_of_day_user(self, tg_id):
        with self.connection:
            time = self.cursor.execute(f"select time_of_day from users where tg_id = ?", (tg_id,)).fetchall()
            return time

    """Получение ежедневных вопросов пользователя"""
    def get_every_day_quests_user(self, tg_id):
        with self.connection:
            time = self.cursor.execute(f"select everyday from users where tg_id = ?", (tg_id,)).fetchall()
            return time
