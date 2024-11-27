# screens/add_edit_task.py
from kivy.uix.screenmanager import Screen
from kivy.app import App

class AddEditTaskScreen(Screen):
    def save_task(self):
        title = self.ids.title_input.text
        description = self.ids.description_input.text
        category = self.ids.category_spinner.text
        due_time = self.ids.due_time_input.text  # Формат: YYYY-MM-DD HH:MM:SS

        app = App.get_running_app()

        if self.manager.current_screen.name == 'add_edit':
            # Додавання нового завдання
            app.db.add_task(title, description, category, due_time)
        else:
            # Редагування існуючого завдання
            task_id = self.task_id
            is_completed = self.is_completed
            app.db.update_task(task_id, title, description, category, due_time, is_completed)

        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def on_pre_enter(self):
        # Очищуємо поля при додаванні нового завдання
        self.ids.title_input.text = ''
        self.ids.description_input.text = ''
        self.ids.category_spinner.text = 'Особисті'
        self.ids.due_time_input.text = ''

    def load_task(self, task):
        self.ids.title_input.text = task[1]
        self.ids.description_input.text = task[2]
        self.ids.category_spinner.text = task[3]
        self.ids.due_time_input.text = task[4]
        self.task_id = task[0]
        self.is_completed = task[5]
