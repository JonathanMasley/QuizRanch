from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import SlideTransition
from shared import ResizableLabel
import json


class calendarScreen(Screen):
    
    def __init__(self, app, **kwargs):
        super(calendarScreen, self).__init__(**kwargs)
        self.app = app  # Store reference to app instance

        # Main layout for the calendar screen
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Top bar layout with back arrow and title
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=1, height=50)

        # Back arrow button
        back_arrow = Button(
            background_normal='leftArrow.png',
            size_hint=(0.3, 0.2),
            pos_hint={'right': 1, 'top': 1},
            on_press=self.go_back_to_front
        )

        # Title label
        label = ResizableLabel(
            text="Calendar",
            font_size_hint=0.05,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.3, 'center_y': 0.9},
            halign='center',
            valign='top',
            color="#FFFFFF"
        )

        # Add widgets to the top bar
        top_bar.add_widget(back_arrow)
        top_bar.add_widget(label)
        top_bar.add_widget(Widget())  # Empty widget for spacing

        # Add top bar to the main layout
        self.add_widget(top_bar)

        # Create a ScrollView
        scroll_view = ScrollView(size_hint=(1, 2), size=(self.width, self.height), do_scroll_x=False, do_scroll_y=True)

        # Create a BoxLayout for events
        self.events_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 50, padding = 20)
        self.events_layout.bind(minimum_height=self.events_layout.setter('height'))
        
        eventsList = load_events_from_file()
        
        if not eventsList:
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
            for event in eventsList:
                event_label = ResizableLabel(
                    text=event,
                    font_size_hint=0.05,
                    size_hint_y=1.5,
                    height=40,
                    halign='left',
                    valign='middle',
                    color="#FFFFFF"
                )
                event_label.bind(size=event_label.setter('text_size'))
                self.events_layout.add_widget(event_label)
                print(f"Added event: {event}")

        # Add events layout to ScrollView
        scroll_view.add_widget(self.events_layout)

        # Add ScrollView to the main layout
        layout.add_widget(Widget())
        layout.add_widget(scroll_view)

        # Add main layout to screen
        
        self.add_widget(layout)
        
        print("Layout added to screen")
    
    
    def go_back_to_front(self, *args):
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'frontPage'


def load_events_from_file(file_name='events.json'):
    """Load the event list from a JSON file."""
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            print("Loaded events:", data)  # Debugging line
            return data
    except FileNotFoundError:
        print("File not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []
