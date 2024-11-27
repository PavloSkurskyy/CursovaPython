# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from database import Database
from kivy.clock import Clock
from plyer import notification
import threading
import time
from datetime import datetime
from kivy.lang import Builder
from os.path import join

# Імпортуємо екрани
from screens.main_screen import MainScreen
from screens.add_edit_task import AddEditTaskScreen
from screens.task_details import TaskDetailsScreen
from screens.task_item import TaskItem  # Імпортуйте TaskItem

class ReminderApp(App):
    def build(self):
        self.db = Database()
        self.sm = ScreenManager()
        # Завантажуємо KV файли
        Builder.load_file(join('kv', 'main_screen.kv'))
        Builder.load_file(join('kv', 'add_edit_task.kv'))
        Builder.load_file(join('kv', 'task_details.kv'))
        # Додаємо екрани
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(AddEditTaskScreen(name='add_edit'))
        self.sm.add_widget(TaskDetailsScreen(name='details'))
        # Запускаємо фоновий потік для перевірки сповіщень
        threading.Thread(target=self.check_notifications, daemon=True).start()
        return self.sm

    def check_notifications(self):
        # Створюємо окремий екземпляр Database для цього потоку
        db_thread = Database()
        while True:
            try:
                tasks = db_thread.get_tasks(completed=False)
                now = datetime.now()
                for task in tasks:
                    try:
                        due_time = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        # Невірний формат дати, пропускаємо завдання
                        print(f"Невірний формат дати для завдання ID {task[0]}")
                        continue
                    if now >= due_time:
                        # Відправляємо сповіщення
                        notification.notify(
                            title=task[1],
                            message=task[2],
                            timeout=10
                        )
                        # Позначаємо завдання як виконане
                        db_thread.update_task(task[0], task[1], task[2], task[3], task[4], 1)
                        # Оновлюємо головний екран у основному потоці
                        Clock.schedule_once(lambda dt: self.sm.get_screen('main').load_tasks())
            except Exception as e:
                print(f"Error in check_notifications: {e}")
            time.sleep(60)  # Перевіряємо кожні 60 секунд

    def show_task_details(self, task_id):
        task = self.db.get_task_by_id(task_id)
        if task:
            self.sm.get_screen('details').set_task(task)
            self.sm.current = 'details'

    def add_task(self):
        self.sm.current = 'add_edit'

    def on_menu(self, instance):
        # Реалізуйте логіку меню, якщо потрібно
        pass

    def toggle_task(self, task_id, is_active):
        task = self.db.get_task_by_id(task_id)
        if task:
            self.db.update_task(
                task_id,
                task[1],  # title
                task[2],  # description
                task[3],  # category
                task[4],  # due_time
                int(is_active)  # is_completed
            )
            self.sm.get_screen('main').load_tasks()

    def on_stop(self):
        # Відключаємо Scheduler при зупинці додатку
        if hasattr(self, 'scheduler') and self.scheduler.running:
            self.scheduler.shutdown()

if __name__ == '__main__':
    ReminderApp().run()
