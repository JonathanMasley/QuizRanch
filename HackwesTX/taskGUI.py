from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from shared import ResizableLabel
from shared import ResizableButton


import json
import os
import random
import time




class taskScreen(Screen):
    def __init__(self, app, **kwargs):
        super(taskScreen, self).__init__(**kwargs)
        self.app = app  # Store reference to app instance for navigation

        # Simple layout for the calendar screen
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top bar to include a back arrow and also the Calendar Screen
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=1, height = 50)
        
        
        # Back arrow button and image
        back_arrow = Button(
            background_normal='leftArrow.png',  # Path to the image file
            size_hint=(0.3, 0.2), #This sizes the image appropriately and allows for dynamic sizing for window size changes
            pos_hint={'right': 1, 'top': 1}, #This positions the image in the top left corner
            on_press=self.go_back_to_front # Once the user presses the button it goes back to the front screen.
        )
        
        # Title label to title the screen
        label = ResizableLabel(text="Tasks",
            font_size_hint=0.05,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.3, 'center_y': 0.9},
            halign='center',
            valign='top',
            color="#FFFFFF"
        )
        
        
        # Adds the back arrow to the top bar layout section
        top_bar.add_widget(back_arrow)
        top_bar.add_widget(label)
        top_bar.add_widget(Widget())

        self.add_widget(top_bar)
        

        # Create a ScrollView
        scroll_view = ScrollView(size_hint=(1, 2), size=(self.width, self.height), do_scroll_x=False, do_scroll_y=True)

        # Create a BoxLayout for events
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = 20)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        
        tasksList = load_tasks_from_file()
        
        if not tasksList:
            no_events_label = ResizableLabel(
                text="No upcoming events.",
                font_size_hint=0.05,
                size_hint_y = 1.5,
                height = 40,
                halign = 'left',
                valign = 'middle',
                color = "#FFFFFF"
            )
            no_events_label.bind(size=no_events_label.setter('text_size'))
            self.events_layout.add_widget(no_events_label)
        else:
            for task in tasksList:
                task_label = ResizableLabel(
                    text=task,
                    font_size_hint=0.05,
                    size_hint_y=1.5,
                    height=40,
                    halign='left',
                    valign='middle',
                    color="#FFFFFF"
                )
                task_label.bind(size=task_label.setter('text_size'))
                self.tasks_layout.add_widget(task_label)
                print(f"Added event: {task}")

        # Add events layout to ScrollView
        scroll_view.add_widget(self.tasks_layout)

        # Add ScrollView to the main layout
        layout.add_widget(Widget())
        layout.add_widget(scroll_view)

        # Add main layout to screen
        
        self.add_widget(layout)
        
        print("Layout added to screen")
    
    
    def go_back_to_front(self, *args):
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'frontPage'


def load_tasks_from_file(file_name='tasks.json'):
    """Load the event list from a JSON file."""
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            print("Loaded tasks:", data)  # Debugging line
            return data
    except FileNotFoundError:
        print("File not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []


