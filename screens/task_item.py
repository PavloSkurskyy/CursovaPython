# screens/task_item.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

class TaskItem(BoxLayout):
    text = StringProperty()
    task_id = NumericProperty()
    is_completed = BooleanProperty()
