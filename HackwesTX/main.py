import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from frontGUI import frontScreen
from calendarGUI import calendarScreen
from taskGUI import taskScreen
from timerclock import TimerClock

import os.path
import datetime
import pytz
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# One scope: googleapis calendar, not read only as we want to create events
# If modifying these scopes, delete the file token.json.
SCOPE_e = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPE_t = ["https://www.googleapis.com/auth/tasks.readonly"]
LOCAL_TIMEZONE = pytz.timezone("America/Chicago")  # Replace with your local timezone

# Customize the window's size and background color
Window.size = (600, 400)  # Width x Height
Window.clearcolor = (33/255, 33/255, 33/255, 1)  # RGBA for grey color


class windowGUI(App):
    def build(self):
        # Screen manager used to switch between screens
        sm = ScreenManager()

        # Initialize the Different Screens
        frontScreen_1 = frontScreen(name='frontPage', app=self)
        calendarScreen_1 = calendarScreen(name='calendarSc', app=self)
        taskScreen_1 = taskScreen(name='taskSc', app=self)
        timerScreen_1 = TimerClock(name='timerSc', app=self)

        # Add the screens to the Screen Manager
        sm.add_widget(frontScreen_1)
        sm.add_widget(calendarScreen_1)
        sm.add_widget(taskScreen_1)
        sm.add_widget(timerScreen_1)

        # Return Screen manager, changes screen by returning 'sm'
        return sm


def events():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token_e.json"):
    creds = Credentials.from_authorized_user_file("token_e.json", SCOPE_e)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPE_e
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token_e.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
            
        )
        .execute()
    )
    events = events_result.get("items", [])
    
    if not events:
      print("No upcoming events found.")
      return
    
    eventList = []
    # Prints the start and name of the next 10 events
    
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      year = start[0:4]
      month = start[5:7]
      day = start[8:10]
      time = start[11:19]
      start = month + "/" + day + "/" + year + " "+ time
      event["start"] = start
      summary = event["summary"]
      event_to_append = start + " " + summary
      eventList.append(event_to_append)
      
      print(event_to_append)
    
      save_events_to_file(eventList)  # Save the events to a file
    
  except HttpError as error:
      print(f"An error occurred: {error}")

def save_events_to_file(events_list, file_name='events.json'):
    """Save the event list to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump(events_list, f)

def tasks():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token_t.json"):
    creds = Credentials.from_authorized_user_file("token_t.json", SCOPE_t)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPE_t
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token_t.json", "w") as token:
      token.write(creds.to_json())
  
  
  try:
      service_tasks = build("tasks", "v1", credentials=creds)
      tasks_result = service_tasks.tasks().list(tasklist="@default").execute()
      tasks = tasks_result.get("items", [])

      if not tasks:
        print("No tasks found.")
      else:
        # Prints the title and due date of the next 10 tasks
        taskList = []
        for task in tasks:
            due = task.get("due", "No due date")
            day_task = due[8:10]
            month_task = due[5:7]
            year_task = due[0:4]
            due_task = month_task + "/" + day_task + "/" + year_task
            title_task = task.get("title", "No title")
            task_to_append = due_task + " " + title_task
            taskList.append(task_to_append)
            
            print(task_to_append)
        save_tasks_to_file(taskList)

        

        
        
  except HttpError as error:
      print(f"An error occurred: {error}")


def save_tasks_to_file(tasks_list, file_name='tasks.json'):
    """Save the task list to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump(tasks_list, f)




# Run the app
if __name__ == '__main__':
    events()
    tasks()
    windowGUI().run()
