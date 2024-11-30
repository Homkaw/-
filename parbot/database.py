import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # Проверяем пользователя в БД
    def check(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM bot_search WHERE id = ?", (id,)).fetchmany(1)

    # Добавляем пользователя
    def add_user(self, id):
        with self.connection:
            return self.cursor.execute("INSERT INTO bot_search ('id') VALUES(?)", (id,))

    # Устанавливаем активность пользователя
    def set_count_post(self, count_post, id):
        with self.connection:
            self.cursor.execute("UPDATE bot_search SET count_post =? WHERE user_id =?", (count_post, id))

    # Устанавливаем активность пользователя
    def set_filter(self, filter, id):
        with self.connection:
            self.cursor.execute("UPDATE bot_search SET filter =? WHERE user_id =?", (filter, id))