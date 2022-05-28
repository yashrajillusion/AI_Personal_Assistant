import pyttsx3  # pip install pyttsx3
import datetime
import speech_recognition as sr #pip install speechRecognition
import wikipedia #pip install wikipedia
import smtplib
import webbrowser as wb
import os
import json
import requests
from urllib.request import urlopen

engine = pyttsx3.init()

engine.runAndWait()


def speak(audio):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()


def register_user():
    file = open('user.txt', 'r')
    user = file.read()
    if user == '':
        speak("I am Jarvis your personal assistant can you register your name")
        file = open('user.txt','w')
        name = input("Enter your name :")
        file.write(name)
        speak("Thanks "+name + "for registering I will call you" + name)
        return ''
    else:
        return user.split()[0]


def time_():
    Time = datetime.datetime.now().strftime('%I:%M')
    speak("The current time is")
    speak(Time)


def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak('The current date is')
    speak(date)
    speak(month)
    speak(year)


def wishme():
    if register_user() != '':
        speak('Welcome back' + register_user())
   # hour = datetime.datetime.now().hour
    speak("Jarvis at your sevice. Please tell me how can i help you today!!")


def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language='en-US')
        print(query)

    except Exception as e:
        print(e)
        print("Say that again please")
        return "None"
    return query


def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    #for this function, you must enable low securtiy in you gmail which you are goin to use as sender

    server.login('skyrakjk1432@gmail.com', 'your password')
    server.sendmail('skyrakjk1432@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishme()
    chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    while True:
        query = TakeCommand().lower()

        #All commands will be stored in lower case in query
        #for easy recognition

        if 'time' in query: # tell us time when asked
            time_()
        elif 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak("Searching...")
            query = query.replace('wikipedia', '')
            result = wikipedia.summary(query, sentences=3)
            speak('According to wikipedia')
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak("what should I say?")
                content = TakeCommand()

                speak('who is the Reciever')
                reciever = input("Enter Email :")
                to = reciever
                sendEmail(to, content)
                speak(content)
                speak("Email has been sent.")

            except Exception as e:
                print(e)
                speak("Unable to send Email.")

        elif 'search in chrome' in query:
            speak('What should I search')
            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')

        elif 'open lms' in query:
            wb.get(chromepath).open_new_tab('https://course.masaischool.com/dashboard')
        elif 'open assignment' in query:
            wb.get(chromepath).open('https://course.masaischool.com/assignments')

        elif 'open youtube' in query:
            speak("What should I search")
            search_term = TakeCommand().lower()
            print('https://www.youtube.com/results?search_query='+search_term)
            speak("Here we go to YOUTUBE!")
            wb.open('https://www.youtube.com/results?search_query=' + search_term)

        elif 'search in google' in query:
            speak('What should I search')
            search_term = TakeCommand().lower()
            wb.open('https://www.google.com/search?q='+search_term)

        elif 'go offline' in query:
            speak("going offline")
            quit()

        elif 'vs' in query:
            speak('Opening'+query+"....")
            path = 'C:/Users/yashr/Desktop/Visual Studio Code.lnk'
            os.startfile(path)

        elif 'write a note' in query or 'create notes' in query:
            speak('What should I write?')
            notes = TakeCommand()
            file = open('notes.txt', 'w')
            speak('Sir should I include Date and Time')
            ans = TakeCommand()

            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime('%H:%M')
                file.write(strTime)
                file.write(':-')
                file.write(notes)

            else:
                file.write(notes)
            speak("Done Taking notes, Sir!")

        elif 'show me the notes' in query:
            speak('showing notes')
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())

        elif 'news' in query:
            try:
                jsonObj = urlopen('https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=740a756fe4d14c48b0ac157b4255a272')
                data = json.load(jsonObj)
                i = 1
                speak("Here are some top headlines from the entainment industry")

                for item in data['articles']:
                    print(item['title'])
                    speak(item['title'])
                    i += 1
                    if i == 5:
                        break


            except Exception as e:
                print(str(e))

        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system('shutdown /r /t l')
        elif 'shutdown' in query:
            os.system('shutdown /s /t l')

#pyinstaller --onefile 'jarvis1.0.py'
#pip install pyintstaller