import sqlite3
from datetime import datetime




class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id BIGINT NOT NULL,
            username varchar(255) NULL,  
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.execute(sql, commit=True)

    def get_all_user_ids(self):
        query = "SELECT telegram_id FROM users"  # 'users' jadvalining nomi
        result = self.execute(query)
        return [row[0] for row in result]


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_all_user_ids(self):
        sql = "SELECT telegram_id FROM Users"
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql)
        ids = [row[0] for row in cursor.fetchall()]
        connection.close()
        return ids

    def add_user(self, telegram_id: int, username: str, created_at=None):
        sql = """
        INSERT INTO Users(telegram_id, username, created_at) VALUES(?, ?, ?)
        """
        if created_at is None:
            created_at = datetime.now()
        self.execute(sql, parameters=(telegram_id, username, created_at), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)


    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)



    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

