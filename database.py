# database.py
import sqlite3

class Database:
    def __init__(self, db_name='tasks.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            due_time TEXT,
            is_completed INTEGER DEFAULT 0
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, title, description, category, due_time):
        query = '''
        INSERT INTO tasks (title, description, category, due_time)
        VALUES (?, ?, ?, ?)
        '''
        self.conn.execute(query, (title, description, category, due_time))
        self.conn.commit()

    def get_tasks(self, completed=None, category=None):
        query = 'SELECT * FROM tasks WHERE 1=1'
        params = []
        if completed is not None:
            query += ' AND is_completed = ?'
            params.append(1 if completed else 0)
        if category:
            query += ' AND category = ?'
            params.append(category)
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def get_task_by_id(self, task_id):
        query = 'SELECT * FROM tasks WHERE id = ?'
        cursor = self.conn.execute(query, (task_id,))
        return cursor.fetchone()

    def update_task(self, task_id, title, description, category, due_time, is_completed):
        query = '''
        UPDATE tasks
        SET title = ?, description = ?, category = ?, due_time = ?, is_completed = ?
        WHERE id = ?
        '''
        self.conn.execute(query, (title, description, category, due_time, is_completed, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        query = 'DELETE FROM tasks WHERE id = ?'
        self.conn.execute(query, (task_id,))
        self.conn.commit()
