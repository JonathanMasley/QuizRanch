from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.widget import Widget
from kivy.graphics import RoundedRectangle, Color

from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from shared import ResizableLabel
from shared import ResizableButton
from shared import ResizableTextInput
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

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
        #used as counter
        self.i = 1
        self.correct = 0
        self.current_case = 0
        self.current_question = 0
        self.fileName = ""
        self.finish = 0 

        # Main layout: FloatLayout to allow free-floating elements
        self.main_layout = FloatLayout()
        self.score_layout = FloatLayout()

        # Structured layout: BoxLayout for label and other buttons
        self.structured_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Label at the top
        #label = Label(text="Welcome to the Main Screen!", font_size=24, size_hint=(1, 0.2))
        #structured_layout.add_widget(label)

        # Button row at the bottom (Timer, Calendar, Task)
        self.button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)

        # Timer Button (fixed size)
        self.timer_button = ResizableButton(text="Timer", font_size_hint=0.05)
        self.timer_button.bind(on_press=self.go_to_timer)
        self.button_layout.add_widget(self.timer_button)

        # Calendar Button (fixed size)
        self.calendar_button = ResizableButton(text="Calendar", font_size_hint=0.05)
        self.calendar_button.bind(on_press=self.go_to_calendar)
        self.button_layout.add_widget(self.calendar_button)

        # Task Button (fixed size)
        self.task_button = ResizableButton(text="Task", font_size_hint = 0.05)
        self.task_button.bind(on_press=self.go_to_task)
        self.button_layout.add_widget(self.task_button)

        # IMAGE
        # Add an image at the top of the screen
        self.img = Image(source='QuizRanch.png', size_hint=(.5, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.85})
        self.main_layout.add_widget(self.img)
        
        # Add the button layout to the structured layout
        self.structured_layout.add_widget(Widget())
        self.structured_layout.add_widget(self.button_layout)

        # Add the structured BoxLayout to the main FloatLayout
        self.main_layout.add_widget(self.structured_layout)

        # Free-floating Button for List (added to FloatLayout)
        self.list_button = ResizableButton(text="Create a List!", font_size=0.05, color='#FFFFFF', size_hint=(0.4, 0.25))
        self.list_button.pos_hint = {'center_x': 0.25, 'center_y':0.5}
        self.main_layout.add_widget(self.list_button)
        self.list_button.bind(on_press=self.get_filename)

        # Free-floating Button for Take Quiz
        self.quiz_button = ResizableButton(text="Take a quiz!", font_size=0.05, color='#FFFFFF', size_hint=(0.4, 0.25))
        self.quiz_button.pos_hint = {'center_x': 0.75, 'center_y':0.5}
        self.main_layout.add_widget(self.quiz_button)
        self.quiz_button.bind(on_press=self.prep_quiz)


        # Set the main layout for the screen
        self.add_widget(self.main_layout)


    def go_to_calendar(self, *args):
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'calendarSc'  # Switch to calendar screen

    def go_to_task(self, *args):
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'taskSc'  # Switch to task screen
        
    def go_to_timer(self, *args):
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'timerSc'  # Switch to timer screen

    def prep_quiz(self, *args):
        # Remove buttons when adding terms
        self.main_layout.remove_widget(self.list_button)
        self.main_layout.remove_widget(self.quiz_button)
        self.main_layout.remove_widget(self.img)

        # Create a ScrollView to contain the list of study sets
        scroll_view = ScrollView(size_hint=(1, None), size=(self.width, 300), do_scroll_x=False, do_scroll_y=True)
    
        # Create a BoxLayout to hold the list of study sets
        self.study_set_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding = 10)
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
            button = ResizableButton(text=set_name, size_hint=(1, None), height=40)  # Create a new Button widget with proper size
            self.buttons.append(button)  # Add the Button to the list of buttons
            button.bind(on_press=self.remove_quizzes)
            self.study_set_layout.add_widget(button)  # Add the Button to the layout
        
        # Add the BoxLayout to the ScrollView
        scroll_view.add_widget(self.study_set_layout)
        
        # Position the ScrollView above the buttons
        scroll_view.pos_hint = {'center_x': 0.5, 'top': 0.9}
        
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
        folder_path = "C:/Users/jonat/Documents/- 5th Semester TTU/HackwesTX/hackathon"
        os.makedirs(folder_path, exist_ok = True)
        file_path = os.path.join(folder_path, buttonPressed)
        with open(file_path, 'r') as file:
            data = json.load(file)

        self.terms = data['Terms']
        self.answers = data['Answers']
        self.cases = data['Amount'][-1]
        self.nonPop = data['Terms']
        self.nonPopAnswers = data['Answers']
        
        self.show_questions()
        

    def show_questions(self, *args):
        if self.i <= self.cases:
            if self.i == 1 or self.i != self.current_question:
                # Get a random term
                term = random.choice(self.terms)
                
                                
                # Update the TextInput's text and make it visible
                self.question = ResizableLabel(text = str(self.i) + ": "+ term, halign='center', font_size_hint = 0.05, color='#FFFFFF')
                self.question.pos_hint = {'center_x' : 0.5, 'center_y': 0.9}
                self.main_layout.add_widget(self.question)


                # Get the index of the term from non-modified list (nonPop)
                term_index = self.nonPop.index(term)
                print(term_index)
                self.correct_answer = self.nonPopAnswers[term_index]
                print('correct answer: ' + self.correct_answer)

                # Remove the selected term from self.terms to avoid duplicates in the next round
                self.terms.remove(term)

                # Create a copy of answers and remove the correct answer
                temp_answer = self.answers[:]
                temp_answer.pop(term_index)

                # Ensure the correct answer is in the list of choices
                selected_answers = [self.correct_answer]

                # Get three more random answers that are not the correct one, without duplicates
                while len(selected_answers) < 4:
                    random_answer = random.choice(temp_answer)
                    temp_answer.remove(random_answer)
                    selected_answers.append(random_answer)

                # Shuffle the answers to randomize their order
                random.shuffle(selected_answers)

                self.a1 = selected_answers[0]
                self.a2 = selected_answers[1]
                self.a3 = selected_answers[2]
                self.a4 = selected_answers[3]
                
                # Create the answer buttons
                self.createAnswer()

    def createAnswer(self, *args):
        # Button for choice A
        self.a_button = ResizableButton(text=self.a1, font_size_hint=0.05, color='#FFFFFF', size_hint=(0.8, .12))
        self.a_button.pos_hint = {'center_x': 0.5, 'center_y':0.3}
        self.main_layout.add_widget(self.a_button)
        self.a_button.bind(on_press=self.next)

        # Button for choice B
        self.b_button = ResizableButton(text=self.a2, font_size_hint=0.05, color='#FFFFFF',size_hint=(0.8, .12))
        self.b_button.pos_hint = {'center_x': 0.5, 'center_y':0.45}
        self.main_layout.add_widget(self.b_button)
        self.b_button.bind(on_press=self.next)

        # Button for choice C
        self.c_button = ResizableButton(text=self.a3, font_size_hint=0.05, color='#FFFFFF', size_hint=(0.8, .12))
        self.c_button.pos_hint = {'center_x': 0.5, 'center_y':0.60}
        self.main_layout.add_widget(self.c_button)
        self.c_button.bind(on_press=self.next)

        # Button for choice D
        self.d_button = ResizableButton(text=self.a4, font_size_hint=0.05, color='#FFFFFF', size_hint=(0.8, .12))
        self.d_button.pos_hint = {'center_x': 0.5, 'center_y':0.75}
        self.main_layout.add_widget(self.d_button)
        self.d_button.bind(on_press=self.next)

        self.current_question = self.i

    def deleteAnswer(self):
        
        self.main_layout.remove_widget(self.a_button)
        self.main_layout.remove_widget(self.b_button)
        self.main_layout.remove_widget(self.c_button)
        self.main_layout.remove_widget(self.d_button)
    #    self.display_score
    
    #def display_score(self, *args):


    def next(self, instance, *args):
        self.main_layout.remove_widget(self.a_button)
        self.main_layout.remove_widget(self.b_button)
        self.main_layout.remove_widget(self.c_button)
        self.main_layout.remove_widget(self.d_button)
        self.main_layout.remove_widget(self.question)
        self.i += 1
        print(f'i {self.i} cases {self.cases}')

        # Check if the button pressed matches the correct answer
        if str(instance.text) == str(self.correct_answer):
            self.correct += 1

        print(f'You got {self.correct} questions correct')

        # Show the next question or handle end of quiz
        if self.i > self.cases:
            self.deleteAnswer()
            print("Quiz completed! Show results or final message here.")
            grade = (self.correct/self.cases)*100
            # Update the TextInput's text and make it visible
            self.gradeOut = ResizableLabel(text = str(grade) + "%", halign='center', font_size_hint = 0.05, color='#FFFFFF')
            self.gradeOut.pos_hint = {'center_x' : 0.5, 'center_y': 0.7}
            self.main_layout.add_widget(self.gradeOut)
            
            # Free-floating Button for Take Quiz
            self.next_button = ResizableButton(text="Next", font_size=0.05, color='#FFFFFF', size_hint=(0.4, 0.25))
            self.next_button.pos_hint = {'center_x': 0.5, 'center_y':0.4}
            self.main_layout.add_widget(self.next_button)
            self.next_button.bind(on_press=self.continueNext)
        else:
            self.show_questions()

    def continueNext(self, *args):
        # Removes the Grade and Next Buttons, reinstantiates the original buttons above.
        self.main_layout.remove_widget(self.next_button)
        self.main_layout.remove_widget(self.gradeOut)
        self.main_layout.add_widget(self.quiz_button)
        self.main_layout.add_widget(self.list_button)
        self.main_layout.add_widget(self.img)


    def get_filename(self, *args):
        # Remove buttons when adding terms
        self.main_layout.remove_widget(self.list_button)
        self.main_layout.remove_widget(self.quiz_button)

        #creates center x
        center_x = (self.width - 300) / 2

        self.filename_input = ResizableTextInput(hint_text="Enter List Name", font_size_hint = 0.05, size_hint=(0.45, 0.12))
        self.filename_input.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        # Add widgets to form layout
        self.main_layout.add_widget(self.filename_input)

        # Submit Button
        self.submit_button = ResizableButton(text="Submit", font_size_hint = 0.05, size_hint=(0.45, 0.12), color = "#FFFFFF")
        self.submit_button.bind(on_press=self.add_terms)
        self.submit_button.pos_hint = {'center_x': 0.5,'center_y': 0.35}
        self.main_layout.add_widget(self.submit_button)



    def add_terms(self, *args):
        #removes file request stuff
        print("GOT TO TERMS")
        self.main_layout.remove_widget(self.submit_button)
        self.main_layout.remove_widget(self.filename_input)
        self.main_layout.remove_widget(self.img)

        # Create and configure the form layout
        self.form_layout = FloatLayout(size=(self.width, self.height))

        # Text Inputs
        self.term_input = ResizableTextInput(hint_text="Enter Term", font_size_hint = 0.05, size_hint=(0.45, 0.12))
        self.term_input.pos_hint = {'center_x': 0.5,'center_y': 0.8}
        self.answer_input = ResizableTextInput(hint_text="Enter Answer", font_size_hint = 0.05, size_hint=(0.45, 0.12))
        self.answer_input.pos_hint = {'center_x': 0.5,'center_y': 0.65}
        
        self.main_layout.add_widget(self.term_input)
        self.main_layout.add_widget(self.answer_input)

        # Submit Button
        self.submitTerm_button = ResizableButton(text="Submit", font_size_hint = 0.05, size_hint=(0.45, 0.12), color = "#FFFFFF")
        self.submitTerm_button.pos_hint = {'center_x': 0.5,'center_y': 0.50}
        self.submitTerm_button.bind(on_press=self.submit_entry)
        self.main_layout.add_widget(self.submitTerm_button)

        # Done Button
        self.done_button = ResizableButton(text="Done", font_size_hint = 0.05, size_hint=(0.45, 0.12), color = "#FFFFFF")
        self.done_button.pos_hint = {'center_x': 0.5,'center_y': 0.35}
        self.done_button.bind(on_press=self.save_and_exit)
        self.main_layout.add_widget(self.done_button)


        # Calculate center position
        center_x = (self.width - 300) / 2

        # Add the form layout to the main layout
        #self.main_layout.add_widget(self.form_layout)

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
        # Remove the term input, answer input, submit button, and done button from main_layout
        self.main_layout.remove_widget(self.term_input)
        self.main_layout.remove_widget(self.answer_input)
        self.main_layout.remove_widget(self.submitTerm_button)
        self.main_layout.remove_widget(self.done_button)

        # Specify folder path
        folder_path = "C:/Users/jonat/Documents/- 5th Semester TTU/HackwesTX/hackathon"

        # Make sure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Create the filename for the JSON file
        filename = self.filename_input.text + '.json'
        fileNoJson = self.filename_input.text

        # Save the dictionary to a file
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w") as outfile:
            json.dump(self.dictionary, outfile)

        # Append the filename (without extension) to 'study_sets.txt'
        data_to_append = fileNoJson + "\n"
        study_set_path = 'study_sets.txt'
        with open(study_set_path, 'a') as file:
            file.write(data_to_append)

        print(f"File saved at: {file_path}")

        # Add back the main buttons
        self.main_layout.add_widget(self.list_button)
        self.main_layout.add_widget(self.quiz_button)
        self.main_layout.add_widget(self.img)
