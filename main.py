import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb

import pyautogui
import webbrowser
import time
import smtplib
from bs4 import BeautifulSoup
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 220)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
USER = config('USER')
HOSTNAME = config('BOT')


def greet():
    print( 'Hi')

def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")

    speak(f"I am {HOSTNAME}. How may i assist you? {USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print("started listening ")


def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir,take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you?" in query:
                speak("i am absloutly fine sir, thanks for asking")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')
            elif "close command prompt" in query:
                speak("Closing command prompt")
                os.system('taskkill /f /im cmd.exe')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:', shell=True)
            elif "close camera" in query:
                speak("Closing camera sir")
                sp.run('taskkill /f /im WindowsCamera.exe', shell=True)


            elif "close notepad" in query:
                speak("Closing Notepad for you sir")
                os.system('taskkill /f /im notepad.exe')


            elif "open steam" in query:
                speak("Opening Steam for you sir")
                discord_path = "C:\\Program Files (x86)\\Steam\\steam.exe"
                os.startfile(discord_path)
            elif "close steam" in query:
                speak("Closing Steam for you sir")
                os.system('taskkill /f /im steam.exe')

            elif "open file explorer" in query:
                speak("Opening file explorer for you sir")
                speak("What should I open for you sir?")
                file = take_command().lower()
                path = "C:\\Users\\Azmat\\" + file.capitalize()
                os.startfile(path)
            elif "close file explorer" in query:
                speak("Closing file explorer for you sir")
                os.system('taskkill /f /im explorer.exe')

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)
            elif "close youtube" in query:
                speak("Closing youtube for you sir")
                os.system('taskkill /f /im msedge.exe')

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)
            elif "close google" in query:
                speak("Closing google for you sir")
                os.system('taskkill /f /im msedge.exe')
            elif "open chrome" in query:
                speak("Opening chrome for you sir")
                chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(chrome_path)
            elif "close chrome" in query:
                speak("Closing chrome for you sir")
                os.system('taskkill /f /im chrome.exe')

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")


                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(), sep='\n')



            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                          f"The plot summary of movie is {plot}")

                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")




            elif "shutdown" in query or "shut down" in query:
                speak("Shutting down the system. Goodbye, sir!")
                os.system("shutdown /s /t 1")
            elif "sleep" in query or "go to sleep" in query:
                speak("Going to sleep, sir!")
                os.system("shutdown /h")
            elif "restart" in query:
                speak("Restarting the system, sir!")
                os.system("shutdown /r /t 1")



            elif "open notepad" in query:
                speak("Opening Notepad for you, sir.")
                os.startfile("C:\\Windows\\notepad.exe")
                time.sleep(1)

                while True:
                    speak("What would you like me to type next? Say 'stop' to finish typing.")
                    text_to_type = take_command()

                    # Remove any existing text up to a certain word (e.g., "clear")
                    if "clear" in text_to_type.lower():
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.press('backspace')
                        speak("Cleared the text.")
                        pyautogui.typewrite(text_to_type + " ", interval=0.1)
                        speak(f"Typed: {text_to_type}")
            elif 'weather' in query:

                ip_address = find_my_ip()

                try:
                    speak("tell me the name of your city")
                    city = take_command().lower()

                except Exception:
                    speak("Sorry I couldn't understand. Can you please repeat that?")

                else:
                    city = take_command().lower()
                    url = "https://www.google.com/search?q=" + "weather" + city
                    html = requests.get(url).content
                    soup = BeautifulSoup(html, 'html.parser')
                    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

                    # Extracting the time and sky description
                    str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
                    data = str_.split('\n')
                    time = data[0]
                    sky = data[1]

                    # Getting all div tags with the specific class name
                    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

                    # Extracting other required data
                    strd = listdiv[5].text
                    pos = strd.find('Wind')
                    other_data = strd[pos:]
                    speak(f"Getting weather report for your city {city}")
                    speak(f"Temperature is:{temp}")
                    speak(f"Time:{time}")
                    speak(f"Sky Description:{sky}")
                    speak(other_data)
            # Voice command to open a specific website
            elif "open website" in query:
                speak("Which website would you like to open, sir?")
                website = take_command().lower()
                url = "https://www." + website + ".com"
                webbrowser.open(url)
                speak(f"Opening {website} website, sir.")

            # Voice command to play music
            elif "play music" in query:
                speak("Which music would you like to play, sir?")
                music = take_command().lower()
                url = "https://www.youtube.com/results?search_query=" + music
                webbrowser.open(url)
                speak(f"Playing {music} music, sir.")
            # Voice command to send a WhatsApp message
            elif "open whatsapp" in query:
                speak("Who would you like to send the message to, sir?")
                contact = take_command().lower()
                speak("What is the message, sir?")
                message = take_command().lower()
                url = "https://api.whatsapp.com/send?phone=" +"+91"+ contact + "&text=" + message
                webbrowser.open(url)
                speak(f"Sending WhatsApp message to {contact}, sir.")
                print(url)

            # Voice command to get the definition of a word
            elif "define" in query:
                speak("Which word would you like to define, sir?")
                word = take_command().lower()
                url = "https://www.google.com/search?q=define+" + word
                webbrowser.open(url)
                speak(f"Defining {word}, sir.")

            # Voice command to get the news updates
            elif "news updates" in query:
                speak("Getting news updates, sir.")
                url = "https://www.google.com/news"
                webbrowser.open(url)
                speak("News updates, sir.")

            # Voice command to get the stock market updates
            elif "stock market updates" in query:
                speak("Getting stock market updates, sir.")
                url = "https://www.google.com/finance"
                webbrowser.open(url)
                speak("Stock market updates, sir.")

            # Voice command to get the cricket score
            elif "cricket score" in query:
                speak("Getting cricket score, sir.")
                url = "https://www.cricbuzz.com/"
                webbrowser.open(url)
                speak("Cricket score, sir.")

            # Voice command to get the football score
            elif "football score" in query:
                speak("Getting football score, sir.")
                url = "https://www.goal.com/en-in/"
                webbrowser.open(url)
                speak("Football score, sir.")

            # Voice command to get the weather forecast for the next 7 days
            elif "weather forecast" in query:
                speak("Getting weather forecast for the next 7 days, sir.")
                url = "https://www.accuweather.com/en/in/"
                webbrowser.open(url)
                speak("Weather forecast for the next 7 days, sir.")

            # Voice command to get the horoscope
            elif "horoscope" in query:
                speak("Getting horoscope, sir.")
                url = "https://www.astroyogi.com/horoscope/"
                webbrowser.open(url)
                speak("Horoscope, sir.")

            # Voice command to get the jokes
            elif "jokes" in query:
                speak("Getting jokes, sir.")
                url = "https://www.jokes.com/"
                webbrowser.open(url)
                speak("Jokes, sir.")

            # Voice command to get the quotes
            elif "quotes" in query:
                speak("Getting quotes, sir.")
                url = "https://www.brainyquote.com/"
                webbrowser.open(url)
                speak("Quotes, sir.")








