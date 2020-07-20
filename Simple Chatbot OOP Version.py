from tkinter import *
from gtts import gTTS
import datetime
import calendar
import random
import wikipedia
import warnings
import sys
import subprocess

class App:
    def __init__(self, master):
        '''Initialise the main Chatbox GUI.

        Parameters
        __________
        No parameters required but global variables are defined

        Return
        ______
        The main GUI.'''
        
        master.title("Chatbot"), master.geometry("300x300"), master.resizable(False, False)
        
        self.userText = StringVar(None)
        self.userTextEntry = Entry(master, textvariable=self.userText, width=25)
        self.userTextEntry.place(x=0, y=272)
        
        self.box = Text(master, bd=1, background="yellow")
        self.box.place(x=0, y=0, width=298, height=273)
        self.box.insert(1.0,"Hello I am your assistant.\nHow can I help you?")

        self.sendButton = Button(master, text="Send", padx=12, pady=3.4,
                                 command=self.enterPressed)
        self.sendButton.place(x=236,y=273)

        self.wakeUpWordsList = ("hey", "hi there", "hello", "greetings", "salutations", "hi", "yo")


    def send(self, userText, isUser):
        '''Return updated conversation on main chat.

        Parameters
        __________
        userText: str, not optional
            User entered text
        isUser: bool, not optional
            True: User, False: Computer
    
        Return
        ______
        Clear user entered entrybox and update user or comp tag on main chatbox.'''
    
        if isUser:
            addOn = "You: "
        else:
            addOn = "Comp: "
        self.userText.set("")
        self.addText(userText, addOn)

    
    def addText(self, userText, addOn):
        '''Return user and computer response onto chatbox.

        Parameters
        __________
        userText: str, not optional
            User entered text
        addOn: str, not optional
            User question or Computer response to add to main chatbox

        Return
        ______
        New updated chat window.'''
    
        final_text = self.box.get("1.0", "end-1c")+"\n"+addOn+userText
        self.box.delete(1.0,"end")
        self.box.insert(1.0, final_text)
        

    def getVoiceResponse(self, compText):
        '''Return Spoken Message to User.

        Parameters
        __________
        userText: str, not optional
            User entered text

        Return:
        Spoken response to user.'''
        
        tts = gTTS(text=compText, lang="en", slow=False)
        tts.save("assistant_response.mp3")
        subprocess.call(["afplay", "assistant_response.mp3"])


    def makeGreeting(self):
        '''Greet User.

        Parameters
        __________
        No Parameters required

        Return
        ______
        Randomly select a greeting to User.'''
        
        word_selected = random.choice(self.wakeUpWordsList)
        return word_selected[0].upper()+word_selected[1:]


    def getPersonName(self, userText):
        '''Return name of person to search from user textfield.

        Parameters
        __________
        userText: str, not optional
            User entered text

        Return
        ______
        Person to search in Wikipedia.'''
        
        textList = userText.split("who is")
        if len(textList) == 0:
            return "Please Try Again."
        return "".join(textList)


    def getTime(self):
        '''Return current time.

        Parameters
        _________
        No Parameters required

        Return
        ______
        Formatted string: It is " 00:00(a.m or p.m)'''
    
        now = datetime.datetime.now()
        meridiem = ""
        if now.hour < 12:
            meridiem = "a.m"
            currentHour = str(now.hour)
        else:
            meridiem = "p.m"
            if now.hour > 12:
                currentHour = str(now.hour - 12)
            else:
                currentHour = str(now.hour)

        if now.minute > 10:
            currentMinute = str(now.minute)
        else:
            currentMinute = "0"+str(now.minute)
        
        return "It is " + currentHour + ":" + currentMinute + meridiem

    
    def getDate(self):
        '''return current date.
        
        Parameters
        __________
        No Parameters required

        Return
        ______
        Date of the runtime.'''
        
        now = datetime.datetime.now()
        year,month,day = str(now.year), now.month - 1, now.day - 1

        date = datetime.datetime.today()
        weekday = calendar.day_name[date.weekday()]

        monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October","November",
                      "December"]
        
        ordinalNumbers = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th",
                          "8th", "9th", "10th", "11th", "12th", "13th", "14th",
                          "15th", "16th", "17th", "18th", "19th", "20th", "21st",
                          "22nd", "23rd", "24th", "25th", "26th", "27th", "28th",
                          "29th", "30th", "31st"]

        return "Today is "+ weekday + " " + ordinalNumbers[day] + " of " + monthNames[month] + " " + str(year)


    def enterPressed(self, event=None):
        '''Return user's processed request.

        Parameters
        __________
        event: <Return>, optional
            user either pressed enter or the dedicated send button

        Return
        ______
        User's processed request.'''
        
        userText = app.userText.get()
        app.send(userText, True)
        compText = ""

        userText = userText.lower()

        if userText in app.wakeUpWordsList:
            compText = app.makeGreeting()
            app.send(compText, False)
            app.getVoiceResponse(compText)
        if "bye" in userText:
            app.getVoiceResponse("Bye")
            root.destroy()
            sys.exit()
        if "date" in userText:
            compText = app.getDate()
            app.send(compText, False)
            app.getVoiceResponse(compText)
        if "time" in userText:
            compText = app.getTime()
            app.send(compText, False)
            app.getVoiceResponse(compText)
        if "who is" in userText:
            #Check for wikipedia.exceptions.DisambiguationError
            try:
                compText = wikipedia.summary(app.getPersonName(userText), sentences=2)
                app.send(compText, False)
                app.getVoiceResponse(compText)
            except wikipedia.exceptions.DisambiguationError:
                app.send("I do not know this person. Please be more precise.", False)
                app.getVoiceResponse("I do not know this person. Please be more precise.")
        elif compText == "":
            #"I do not understand" error checks
            app.send("I do not understand. Please try again.", False)
            app.getVoiceResponse("I do not understand. Please try again.")


#Create App object and start chatbot program
root = Tk()
app = App(root)
warnings.filterwarnings("ignore")

#Check if enter button pressed
app.userTextEntry.bind('<Return>',app.enterPressed)
root.mainloop()
