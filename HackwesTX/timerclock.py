from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import SlideTransition
from datetime import datetime, timedelta
import re, kivy, pytz
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from shared import ResizableLabel
from shared import ResizableButton
from kivy.factory import Factory as F
from functools import partial
from kivy.app import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.core.window import Window
from time import strftime
from shared import ResizableTextInput
from shared import ResizableButton


class TimerClock(Screen):
    def __init__(self, app, **kwargs):
        super(TimerClock, self).__init__(**kwargs)
        self.app = app

        # Initialization of Control Variables
        self.running = False
        self.total_seconds = 0
        self.start_time = None
            
        #layout
        main_layout = BoxLayout(orientation='vertical', size_hint_y = 1, height = 100, width = 50, padding=20, spacing=20)
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=1, height=50)
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=1, height=100, padding=20, spacing=20)

        #top label
        label = ResizableLabel(
            text="Timer",
            font_size_hint=0.05,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.3, 'center_y': 0.9}, 
            halign='center',
            valign='top',
            color="#FFFFFF"
        )
        
        # timer box
        timer_box = BoxLayout(orientation='vertical')
        input_box = BoxLayout(orientation = 'horizontal')
        self.time_question = ResizableLabel(text='Enter the time to count down: ', halign='center', font_size_hint = 0.05, color='#FFFFFF')
        self.time_input = ResizableTextInput(text="00:00", halign='center', size_hint = (0.9,0.7), font_size_hint = 0.05) 
        timer_box.add_widget(self.time_question)
        input_box.add_widget(Widget())
        input_box.add_widget(self.time_input)
        input_box.add_widget(Widget())
        timer_box.add_widget(input_box)

        #buttons layout
        self.start_button = ResizableButton(text="Start", font_size_hint=0.05, color = "#FFFFFF")
        self.start_button.bind(on_press=self.toggle)
        
        # Back arrow button and image
        back_arrow = Button(
            background_normal='leftArrow.png',  # Path to the image file
            size_hint=(0.3, 0.2), #This sizes the image appropriately and allows for dynamic sizing for window size changes
            pos_hint={'right': 1, 'top': 1}, #This positions the image in the top left corner
            on_press=self.go_back_to_front # Once the user presses the button it goes back to the front screen.
        )
        
        top_bar.add_widget(back_arrow)
        top_bar.add_widget(label)
        top_bar.add_widget(Widget())
        
        input_layout.add_widget(self.start_button)

        main_layout.add_widget(Widget())
        main_layout.add_widget(timer_box)
        main_layout.add_widget(input_layout)
        self.add_widget(top_bar)
        self.add_widget(main_layout)
    
    def toggle(self, *args):
        if self.running:
            self.reset()
        else:
            self.start()

    def start(self, *args):
        # Parse the time input
        try:
            time_parts = self.time_input.text.split(':')
            minutes = int(time_parts[0])
            seconds = int(time_parts[1])
            self.total_seconds = minutes * 60 + seconds
        except ValueError:
            self.time_question.text = 'Invalid time format. Use MM:SS.'
            return

        self.running = True
        self.start_time = datetime.now()
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        elapsed = datetime.now() - self.start_time
        elapsed_seconds = elapsed.total_seconds()
        remaining_seconds = self.total_seconds - elapsed_seconds

        if remaining_seconds <= 0:
            self.time_input.text = '00:00'
            self.time_question.text = "Take a Break!"
        else:
            minutes, seconds = divmod(int(remaining_seconds), 60)
            self.time_input.text = f"{minutes:02}:{seconds:02}"

    def reset(self, *args):
        self.running = False
        self.total_seconds = 0
        self.start_time = None
        self.time_input.text = '00:00'
        self.time_question.text = 'Enter the time to count down: '
        Clock.schedule_interval(self.update_timer, 1)
        
    def go_back_to_front(self, *args):
         # Switch back to the front screen
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'frontPage'
        
