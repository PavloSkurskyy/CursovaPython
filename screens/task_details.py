# screens/task_details.py
from kivy.uix.screenmanager import Screen
from kivy.app import App

class TaskDetailsScreen(Screen):
    selected_task = None

    def set_task(self, task):
        self.selected_task = task
        self.ids.title_label.text = task[1]
        self.ids.description_label.text = task[2]
        self.ids.category_label.text = task[3]
        self.ids.due_time_label.text = task[4]

    def mark_completed(self):
        task = self.selected_task
        app = App.get_running_app()
        app.db.update_task(task[0], task[1], task[2], task[3], task[4], 1)
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def edit_task(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'add_edit'
        app = App.get_running_app()
        app.sm.get_screen('add_edit').load_task(self.selected_task)

    def delete_task(self):
        task = self.selected_task
        app = App.get_running_app()
        app.db.delete_task(task[0])
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'
