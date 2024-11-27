# screens/main_screen.py
from kivy.uix.screenmanager import Screen
from kivy.app import App

class MainScreen(Screen):
    def on_pre_enter(self):
        self.load_tasks()

    def load_tasks(self):
        self.ids.rv.data = []
        app = App.get_running_app()
        tasks = app.db.get_tasks()
        for task in tasks:
            self.ids.rv.data.append({
                'text': f"{'[x] ' if task[5] else '[ ] '} {task[1]} - {task[4]}",
                'task_id': task[0],
                'is_completed': task[5]
            })
