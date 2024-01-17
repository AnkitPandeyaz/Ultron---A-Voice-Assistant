import os
import pygame
import pyttsx3
import webbrowser
import random
import speech_recognition as sr
import datetime
from selenium import webdriver
import subprocess
import time
import geocoder
import geopy.geocoders
import psutil
import cv2
import numpy as np
import pyautogui
import mediapipe as mp



def recognize_speech():
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything...... :")
        audio = recognize.listen(source)
        
    try:
        print("Recognizing...")
        query = recognize.recognize_google(audio, language= 'en -IN')
        print("You said: ", query)
        return query.lower()
    except sr.UnknownValueError:
        respond("Sorry, could not understand the audio.")
        return ""
    
    except sr.RequestError as e:
        print(f"could not request from Google speetch recognition service; {e}")
        return""
    
def respond(text):
    engine= pyttsx3.init()
    engine.setProperty('rate',150)
    engine.setProperty('volume',1.0)
    engine.say(text)
    engine.runAndWait()
    
def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S %p")
    return f"The Current time is{current_time}."

def open_website(url):
    webbrowser.open(url)
    return f"Opening your website sir."
    
def open_application(app_name):
    try:
        os.system(app_name)
        respond(f"Opening {app_name}")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        respond(f"Sorry, I couldn't open {app_name}")

def get_weather(city):
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    base_url = "http://openweathermap.org/current"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
def open_google_maps(location, destination):
    url = f"https://www.google.com/maps/dir/{location}/{destination}"
    webbrowser.open(url)
    respond(f"Opening Google Maps for directions from {location} to {destination}.")

def set_reminder(message, time_str):
    current_time = datetime.datetime.now()
    try:
        reminder_time = datetime.datetime.strptime(time_str, "%H %M %p")
        reminder_time = reminder_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)

        if reminder_time > current_time:
            time_difference = (reminder_time - current_time).total_seconds()
            time.sleep(time_difference)
            respond(f"Reminder: {message}")
        else:
            respond("Invalid reminder time. Please provide a future time.")

    except ValueError:
        respond("Invalid time format. Please use the format like '5:30 PM'.")

def quiz_game(questions):
    score = 0

    for question, answer in questions.items():
        respond(question)
        user_answer = recognize_speech()

        if user_answer == answer:
            respond("Correct!")
            score += 1
        else:
            respond(f"Sorry, the correct answer is {answer}.")

    respond(f"Your final score is {score}/{len(questions)}.")

def save_note(note_text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"note_{timestamp}.txt"

    with open(filename, 'w') as file:
        file.write(note_text)

    print(f"Note saved as {filename}")
    
def organize_notes():
    notes_directory = "notes"
    if not os.path.exists(notes_directory):
        os.makedirs(notes_directory)

    return notes_directory


def get_user_location():
    # Using the geocoder library to get the user's location based on IP address
    user_location = geocoder.ip('me')

    # Extracting latitude and longitude from the location object
    latitude = user_location.latlng[0]
    longitude = user_location.latlng[1]

    return latitude, longitude

def get_location_name(latitude, longitude):
    try:
        geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
        location = geolocator.reverse((latitude, longitude), language="en")
        address = location.address
        return address
    except Exception as e:
        print(f"Error getting location name: {e}")
        return None

def close_all_browsers():
    # List of common browser process names
    browser_process_names = ["chrome", "firefox", "msedge", "iexplore", "opera", "safari" ,"brave", "microsoft bing"]

    for process in psutil.process_iter(['pid', 'name']):
        if any(browser_name in process.info['name'].lower() for browser_name in browser_process_names):
            try:
                # Terminate the browser process
                psutil.Process(process.info['pid']).terminate()
                print(f"Closed browser process: {process.info['name']}")
            except Exception as e:
                print(f"Error closing browser process: {e}")


def hand_gesture_control():
    cap = cv2.VideoCapture(0)
    hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    with hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_tip = hand_landmarks.landmark[hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[hands.HandLandmark.THUMB_TIP]

                    # Check if thumb and index finger are close to each other
                    if cv2.norm(
                        (index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
                    ) < 0.05:
                        pyautogui.scroll(1)  # Scroll down
                    else:
                        pyautogui.scroll(-1)  # Scroll up

            mp_drawing.draw_landmarks(frame, hand_landmarks, hands.HAND_CONNECTIONS)
            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    respond("I'am Ultron, your voice assistant. How may I assist you today?") 
    
    while True:
        user_input = recognize_speech()
        
        if "hello" in user_input or "hey" in user_input or "good morning" in user_input or "morning" in user_input:
            respond("Hello Sir! How are you? How Can I be of service?")
        elif "goodbye" in user_input or "close" in user_input or "good night" in user_input:
            respond("See you soon sir! Have a great Day.")
            break
        
        elif "how are you" in user_input:
            respond("I am functioning properly. Thank You for asking.")
        elif "love you" in user_input:
            respond("Aww, thank you so much! I love you too!")
        
        elif "ultron" in user_input or "Ultron" in user_input:
            respond("Yes sir. I am listening...")
        elif "who are you?" in user_input or "who you are" in user_input or "tell me about yourself" in user_input:
            respond("I am Ultron, your AI assistant, designed to streamline tasks and assist you efficiently. Utilizing advanced natural language processing and speech recognition, I can provide information, open applications, play music, and more. Your commands shape my actions as I strive to enhance your daily experiences through seamless interaction.")
            
        elif "what work you do for me" in user_input or "what you do for me" in user_input or "how you work for me" in user_input or "work you do for me" in user_input:
            respond("Ultron, I am here to simplify your life. Command me to open applications, provide weather updates, play music, or search the web. With speech recognition and natural language processing, I strive to cater to your every need, making tasks effortless and information readily accessible. Your satisfaction is my priority.")
            
        elif "your purpose" in user_input:
            respond("My purpose is to assist you with your daily needs.")
            
        elif"what is time" in user_input or "time" in user_input or "what time" in user_input or "tell me time" in user_input:
            respond(get_time())
               
        elif "open website" in user_input or"open google chrome" in user_input or "hey google" in user_input or "hello google" in user_input or "open google" in user_input or "google" in user_input or "open chrome" in user_input:
            url="https://www.google.com"
            respond(open_website(url))
            
        elif"search me for" in user_input or "search for" in user_input:
            search_query = user_input.replace("search", "").strip()
            respond(f"Searching the web for {search_query}")
            open_website(f"https://www.google.com/search?q={search_query}")
        
        elif "open paint" in user_input:
            open_application("mspaint")

        elif "open camera" in user_input:
            open_application("start microsoft.windows.camera:")
        

        if "notepad" in user_input or "open notepad"in user_input:
            respond("Opening Notepad.")
            os.startfile("notepad.exe")
            
        elif "calculator" in user_input or "open calculator" in user_input:
             respond("Opening Calculator.")
             os.startfile("calc.exe")
             
        elif "weather update" in user_input:
            respond("Sure, please tell me the city for the weather update.")
            city = recognize_speech()  # Assuming the user says the city after the prompt
            weather_update = get_weather(city)
            respond(weather_update)
            
        elif "navigate to" in user_input or "directions from" in user_input:
            respond("Sure, please tell me the starting location.")
            start_location = recognize_speech()  # Assuming the user says the starting location after the prompt
            respond("Now, please tell me the destination.")
            end_location = recognize_speech()  # Assuming the user says the destination after the prompt
            open_google_maps(start_location, end_location)
            
        if "remind me to" in user_input or "set time" in user_input:
            try:
                reminder_message = user_input.split("remind me to")[1].strip()
                respond("Sure, at what time?")
                reminder_time_input = recognize_speech()
                set_reminder(reminder_message, reminder_time_input)

            except IndexError:
                respond("I couldn't understand the reminder message.")
                
        elif "quiz game" in user_input:
             respond("Welcome to the Voice-Activated Quiz Game!")
    
             quiz_questions = {
                "What is the capital of India?": "Delhi",
                "Which planet is known as the Red Planet?": "mars",
                "What is the largest mammal in the world?": "blue whale",
                # Add more questions as needed
                }
             quiz_game(quiz_questions)
             
             
        elif "make notes" in user_input:
            respond("Welcome to the Voice Note-Taking System!")
            notes_directory = organize_notes()

            while True:
                respond("Please speak your note or say 'exit' to end.")
                note_text = recognize_speech()

                if note_text == "exit":
                    respond("Exiting the Voice Note-Taking System. Goodbye!")
                    break
                save_note(note_text)
        
        
        if "my location" in user_input or "location" in user_input or "find me" in user_input:
            location = get_user_location()
            if location:
                respond(f"Your current location - Latitude: {location[0]}, Longitude: {location[1]}")
                location_name = get_location_name(location[0], location[1])
                if location_name:
                    respond(f"Location Name: {location_name}")
                else:
                    respond("Unable to retrieve location name.")
            else:
                respond("Unable to retrieve your location.")

        elif "exit" in user_input:
            respond("Exiting.")
            break
        
        elif "browser" in user_input:
            respond("Closeing all browser sir!")
            close_all_browsers()
        
        elif "handle Website" in user_input or "website" in user_input:
            respond("Controling website hand mode on")
            hand_gesture_control()

            
             
        
        
            
        