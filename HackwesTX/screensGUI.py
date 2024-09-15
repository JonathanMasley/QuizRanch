from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from shared import ResizableLabel
from shared import ResizableButton

import json
import os
import random
import time

class frontScreen(Screen):
    def __init__(self, app, **kwargs):
        super(frontScreen, self).__init__(**kwargs)
        self.app = app  # Store reference to app instance for navigation

        # Initialize variables
        self.dictionary = {
            "Terms": [],
            "Answers": [],
            "Amount": []
        }
        self.count = 1
        self.fileName = ""

        # Main layout: FloatLayout to allow free-floating elements
        self.main_layout = FloatLayout()

        # Structured layout: BoxLayout for label and other buttons
        structured_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Button row at the bottom (Timer, Calendar, Task)
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)

        # Add the button layout to the structured layout
        structured_layout.add_widget(button_layout)

        # Add the structured BoxLayout to the main FloatLayout
        self.main_layout.add_widget(structured_layout)

        # Free-floating Button for List (added to FloatLayout)
        self.list_button = ResizableButton(text="Create a List!", font_size_hint=0.05, color='#000000', size_hint=(None, None), size=(200, 100))
        self.list_button.pos = (100, 250)  # Center-ish and shifted left
        self.main_layout.add_widget(self.list_button)
        self.list_button.bind(on_press=self.get_filename)

        # Free-floating Button for Take Quiz
        self.quiz_button = ResizableButton(text="Take a quiz!", font_size_hint=0.05, color='#000000', size_hint=(None, None), size=(200, 100))
        self.quiz_button.pos = (400, 250)  # Center-ish and shifted left
        self.main_layout.add_widget(self.quiz_button)
        self.quiz_button.bind(on_press=self.prep_quiz)

        # Add a TextInput for displaying text, initially hidden
        self.update_text_input = TextInput(text='', font_size=18, size_hint=(None, None), size=(300, 50), readonly=True)
        self.update_text_input.pos = (self.width / 2 - self.update_text_input.width / 2, self.height / 5)
        self.update_text_input.opacity = 0  # Hide the TextInput initially
        self.main_layout.add_widget(self.update_text_input)

        # Set the main layout for the screen
        self.add_widget(self.main_layout)


    def go_to_calendar(self, *args):
        self.app.root.current = 'calendarSc'  # Switch to calendar screen

    def go_to_task(self, *args):
        self.app.root.current = 'taskSc'  # Switch to task screen

    def prep_quiz(self, *args):
        # Remove buttons when adding terms
        self.main_layout.remove_widget(self.list_button)
        self.main_layout.remove_widget(self.quiz_button)

        # Create a ScrollView to contain the list of study sets
        scroll_view = ScrollView(size_hint=(None, None), size=(self.width, self.height - 300), do_scroll_x=False, do_scroll_y=True)
        
        # Create a BoxLayout to hold the list of study sets
        self.study_set_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.study_set_layout.bind(minimum_height=self.study_set_layout.setter('height'))

        # Example study sets, replace with your actual study set retrieval
        study_sets = []

        with open('study_sets.txt', 'r') as file:
            for line in file:
                stripped_line = line.strip()  # Remove leading/trailing whitespace
                study_sets.append(stripped_line)  # Add the cleaned line to the list
        
        i = 0
        self.buttons = []  # Initialize an empty list to hold button widgets

        for set_name in study_sets:
            button = ResizableButton(text=set_name, font_size_hint = 0.05, size_hint_y=None, height=40)  # Create a new Button widget
            self.buttons.append(button)  # Add the Button to the list of buttons
            button.bind(on_press = self.remove_quizzes)

            #self.submit_button.bind(on_press=self.add_terms)
            self.study_set_layout.add_widget(button)  # Add the Button to the layout
            i += 1  # Increment the index (if you need to use it later)
        
        print(self.buttons)
        # Add the BoxLayout to the ScrollView
        scroll_view.add_widget(self.study_set_layout)
        
        # Position the ScrollView above the buttons
        scroll_view.pos = (0, 200)
        
        # Add the ScrollView to the main layout
        self.main_layout.add_widget(scroll_view)
    def remove_quizzes(self, button, *args):
        self.buttonPressed = button.text
        print(self.buttonPressed)
        #removes button
        for i in self.buttons:
         self.study_set_layout.remove_widget(i)

        self.create_quiz()

    def create_quiz(self, *args):
        buttonPressed = str(self.buttonPressed) + ".json"
        with open(buttonPressed, 'r') as file:
            data = json.load(file)

        self.terms = data['Terms']
        self.answers = data['Answers']
        self.cases = data['Amount'][-1]
        self.correct = 0
        self.current_case = 0

        # Update the TextInput's text and make it visible
        self.update_text_input.text = "New text for the label!"
        self.update_text_input.opacity = 1  # Make the TextInput visible
        self.update_text_input.center = (self.width / 2, self.height / 5)  # Center the TextInput

    def get_filename(self, *args):
        # Remove buttons when adding terms
        self.main_layout.remove_widget(self.list_button)
        self.main_layout.remove_widget(self.quiz_button)

        #creates center x
        center_x = (self.width - 300) / 2

        self.filename_input = TextInput(hint_text="Enter List Name", size_hint=(None, None), size=(300, 40))
        self.filename_input.pos = (center_x, 350)
        # Add widgets to form layout
        self.main_layout.add_widget(self.filename_input)

        # Submit Button
        self.submit_button = ResizableButton(text="Submit", font_size_hint = 0.05, size_hint=(None, None), size=(300, 40))
        self.submit_button.bind(on_press=self.add_terms)
        self.submit_button.pos = (center_x, 300)
        self.main_layout.add_widget(self.submit_button)



    def add_terms(self, *args):
        #removes file request stuff
        self.main_layout.remove_widget(self.submit_button)
        self.main_layout.remove_widget(self.filename_input)

        # Create and configure the form layout
        self.form_layout = FloatLayout(size=(self.width, self.height))

        # Text Inputs
        self.term_input = TextInput(hint_text="Enter term", size_hint=(None, None), size=(300, 40))
        self.answer_input = TextInput(hint_text="Enter answer", size_hint=(None, None), size=(300, 40))

        # Submit Button
        self.submit_button = ResizableButton(text="Submit", font_size_hint = 0.05, size_hint=(None, None), size=(300, 40))
        self.submit_button.bind(on_press=self.submit_entry)

        # Done Button
        self.done_button = ResizableButton(text="Done", font_size_hint = 0.05, size_hint=(None, None), size=(300, 40))
        self.done_button.bind(on_press=self.save_and_exit)

        # Calculate center position
        center_x = (self.width - 300) / 2

        # Position the widgets
        self.term_input.pos = (center_x, 400)
        self.answer_input.pos = (center_x, 350)
        self.submit_button.pos = (center_x, 300)
        self.done_button.pos = (center_x, 250)

        # Add widgets to form layout
        self.form_layout.add_widget(self.term_input)
        self.form_layout.add_widget(self.answer_input)
        self.form_layout.add_widget(self.submit_button)
        self.form_layout.add_widget(self.done_button)

        # Add the form layout to the main layout
        self.main_layout.add_widget(self.form_layout)

    def submit_entry(self, instance):
        term = self.term_input.text
        answer = self.answer_input.text

        if term and answer:
            self.dictionary["Terms"].append(term)
            self.dictionary["Answers"].append(answer)
            self.dictionary["Amount"].append(len(self.dictionary["Terms"]))
            self.term_input.text = ""
            self.answer_input.text = ""
        else:
            print("Both term and answer are required!")

    def save_and_exit(self, instance, *args):
        # Specify folder path
        self.form_layout.remove_widget(self.term_input)
        self.form_layout.remove_widget(self.answer_input)
        self.form_layout.remove_widget(self.submit_button)
        self.form_layout.remove_widget(self.done_button)

        folder_path = "D:/hackathon"  # Replace with your folder path

        # Make sure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        #creates name of file
        filename = self.filename_input.text + '.json'
        fileNoJson = self.filename_input.text

        print(self.filename_input)
        # Save the dictionary to a file
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w") as outfile:
            json.dump(self.dictionary, outfile)

        #write file name to a txt file which will be turned into a list
        data_to_append = fileNoJson +"\n"

        file_path = 'study_sets.txt'

        with open(file_path, 'a')as file:
            file.write(data_to_append)

        print(f"File saved at: {file_path}")

        self.main_layout.add_widget(self.list_button)
        self.main_layout.add_widget(self.quiz_button)