print("\n###########################################################\n### Initiating Parti Gábor's Primitive PDF Audio Reader ###\n###########################################################\n")
  
print("Instructions:\n - Put a pdf in the specified folder.\n - A quick setup will follow with 5 options: voice, speed, path, document, and page; you have to input your settings.\n - Press enter for the default settings.\n\nDependencies: You will also need these two packages: PyPDF2, pyttsx3.")

# %pip install pyttsx3
# %pip install PyPDF2
# %pip install pygame

import easygui
import os
import sys
import glob
import pandas as pd
import numpy as np
import regex as re
import time
import PyPDF2
import pyttsx3
# from pygame import mixer

### Use auto-py-to-exe to make exe ###

# setup engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# voice
# engine.setProperty('voice', voices[1].id)

# select voice
print("\n1. Select voice. Type 'f' or 'm' for a female or a male voice. (Default is female.)")
voice_choice = str(input("Please select voice (f/m): ")) or "f"

if voice_choice == "m":
  engine.setProperty('voice', voices[0].id)
  print("\tOK, loading robotic male voice engine.")
elif voice_choice == "f": 
  engine.setProperty('voice', voices[1].id)
  print("\tOK, loading robotic female voice engine.")
else:
  engine.setProperty('voice', voices[1].id)
  print("\tOops, you have failed to hit any of the right keys, ...loser. Now you have to start again.")
  exit()



# speed
# engine.setProperty('rate', 200)

# select speed
print("\n2. Select speed. Enter a value between 120 and 300 words per minute. (Default is 200 wpm.)")
speed_choice = input("Please enter speed: ") or "200"
engine.setProperty('rate', int(speed_choice))
print("\tOK, loading requested reading rate of", speed_choice, "wpm.")



### Paths ###

# relative path (current folder)
# path = sys.path[0] # does not work with auto-py-to-exe

# absolute path (local)
print("\n3. Select files' directory.")
path = "C:\\Users\\parti\\OneDrive - The Hong Kong Polytechnic University\\[READ]\\Aloud\\"
path_choice = input('Please enter path, such as "C:\\Users\\user\\read\\"') or path
print(path)

# list of pdfs in relative  directory
# pdfs = glob.glob("*.pdf")

# list of pdfs in absolute directory
pdfs = []
os.chdir(path)
for file in glob.glob("*.pdf"):
    pdfs.append(file)



# file
# book_choice = pdfs[0]

# select file
print("\n4. Please select a pdf. Enter the filename here, with extension. (Default is the first pdf alphabetically.)")
book_choice = str(input("Please enter filename: ")) or pdfs[0]



### Parsing ###

# creating a pdf file object
pdfFileObj = open(path+"\\"+book_choice, 'rb')

print("\tParsing book:", path+"\\"+book_choice,"\n\tThis might take some time if your document is several hundred pages long...")

# initialize dataframe to hold documents
df = pd.DataFrame(columns=['page_no', 'page'])

print("\t1/3...")

# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False) 
pages = pdfReader.numPages

print("\t2/3...")

for p in range(pages):
  pageObj = pdfReader.getPage(p)
  # print(p)
  df.loc[p, 'page_no'] = p+1
  page_content = pageObj.extractText()
  # print(page_content)
  df.loc[p, 'page'] = page_content

print("\t3/3...")

#closing the pdf file object 
pdfFileObj.close() 

print("\tPages found:",df.shape[0])
df['page'].replace('', np.nan, inplace=True)
df.dropna(subset=['page'], inplace=True)
df.reset_index(drop=True, inplace=True)

# printing number of pages in pdf file 
print("\tDropping empty ones... Done.\n\tTotal number of pages are", str(df.shape[0]))
time.sleep(1)
print("\tCleaning some of the mess...")

df['page'] = [re.sub(r'\n+', " ", str(x)) for x in df['page']]
df['page'] = [re.sub(r"([a-z])([A-Z])", r"\1 \2", str(x)) for x in df['page']]
df['page'] = [re.sub(r"([A-Z]{2,})([a-z])", r"\1 \2", str(x)) for x in df['page']]
df['page'] = [re.sub(r"([0-9])([A-Z])", r"\1 \2", str(x)) for x in df['page']]
df['page'] = [re.sub(r"([A-Z])([0-9])", r"\1 \2", str(x)) for x in df['page']]
df['page'] = [re.sub(r"([0-9])([a-z])", r"\1 \2", str(x)) for x in df['page']]
df['page'] = [re.sub(r"(\))([A-Z])", r"\1 \2", str(x)) for x in df['page']]
df['page'] = [re.sub(r'– +', "–", str(x)) for x in df['page']]
# df['page'] = [re.sub(r'\n', " ", str(x)) for x in df['page']]
df['page'] = [re.sub(r'\s+', " ", str(x)) for x in df['page']]

content = " ".join(df['page'].tolist())

print("\n5. Do you want to continue where you have left off?\nIf yes, please enter a page number, if no, hit enter.")
page_choice = input("Please enter page number: ") or "0"
page_choice = int(page_choice)
print("\tPage", str(page_choice), "selected, flipping to the page now...")
time.sleep(1)

# cutoff before start
df = df.iloc[page_choice: , :]

# estimate
word_counts = df["page"].apply(lambda n: len(n.split()))
minutes = word_counts.sum() / 200 #estimate
seconds = minutes* 60

def convert_to_preferred_format(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60
   return "%02d:%02d:%02d" % (hour, min, sec) 

print("\nEstimated time of the audio:", convert_to_preferred_format(seconds))
time.sleep(1)

# print("\nGo!\n")
# df.head(20)


#play
for i, row in df.iterrows():
    print("\n# PAGE NO.", str(i), "#")
    print(row['page'])
    engine.say(row['page']) # to read immediately
    engine.runAndWait()

print("Book finished!")
import pyttsx3
def onStart(name):
   print('starting', name)
def onWord(name, location, length):
    print ('word', name, location, length)
    if location > 5:
      engine.stop()
    if keyboard.is_pressed("esc"):
       engine.stop()
def onEnd(name, completed):
   print('finishing', name, completed)
engine = pyttsx3.init()
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()
engine.stop()
import pyttsx3
import time

engine = pyttsx3.init()
engine.startLoop(False)

engine.say("knock knock, who's there")

start = time.time()

while time.time() - start < 1:
    engine.iterate()
    time.sleep(.01)

engine.stop()
engine.say('interrupting cow!')

while time.time() - start < 10:
    engine.iterate()
    time.sleep(.01)

engine.endLoop()
import multiprocessing
import pyttsx3
import keyboard

def sayFunc(phrase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(phrase)
    engine.runAndWait()

def say(phrase):
	if __name__ == "__main__":
		p = multiprocessing.Process(target=sayFunc, args=(phrase,))
		p.start()
		while p.is_alive():
			if keyboard.is_pressed('q'):
				p.terminate()
			else:
				continue
		p.join()

say("this process is running right now")
import multiprocessing
import pyttsx3
import time
from threading import Thread


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def speak(phrase):
    engine = pyttsx3.init()
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()

def stop_speaker():
    global term
    term = True
    t.join()

@threaded
def manage_process(p):
	global term
	while p.is_alive():
		if term:
			p.terminate()
			term = False
		else:
			continue

	
def say(phrase):
	global t
	global term
	term = False
	p = multiprocessing.Process(target=speak, args=(phrase,))
	p.start()
	t = manage_process(p)
		
if __name__ == "__main__":
	say("this process is running right now")
	time.sleep(1)
	stop_speaker()
	say("this process is running right now")
	time.sleep(1.5)
	stop_speaker()
# End
# say = 'getting details of current voice'
# voices = engine.getProperty('voices')      
# # engine.setProperty('volume',1.0)    
# engine.setProperty('voice', voices[1].id)  
# engine.setProperty('rate', 200)     # setting up new voice rate
# outfile = "temp.wav"
# engine.save_to_file(say, outfile)
# engine.runAndWait()
  
# mixer.init()
# mixer.music.load("temp.wav")
# mixer.music.play()


# def stop():
#     mixer.music.stop()

# def pause():
#     mixer.music.pause()

# def unpause():
#     mixer.music.unpause()

 
# while True:
      
#     print("Press 'p' to pause, 'r' to resume")
#     print("Press 'e' to exit the program")
#     query = input("  ")
      
#     if query == 'p':
#         pause() 
#     elif query == 'r':
#         unpause() 
  
#     elif query == 'e':
#         mixer.music.stop()
#         break
# # a function to walk through all files in folder and subfolders
# def list_files(dir):                                                                                                  
#     r = []                                                                                                            
#     subdirs = [x[0] for x in os.walk(dir)]                                                                            
#     for subdir in subdirs:                                                                                            
#         files = os.walk(subdir).__next__()[2]                                                                             
#         if (len(files) > 0):                                                                                          
#             for file in files:                                                                                        
#                 r.append(os.path.join(subdir, file))                                                                         
#     return r
# assign relative directory
# directory = os.path.join(sys.path[0], "data") ### INPUT FOLDER HERE ###
# print("Your input directory is:", directory)

# # list files in directory
# files_in_dir = list_files(directory)
# # files_in_dir = os.listdir(directory)

# # count files in directory
# print("Number of files:",len(files_in_dir))
# Google Text-to-Speech

# https://gtts.readthedocs.io/en/latest/
# %pip install gtts
# Import the required module for text 
# to speech conversion
from gtts import gTTS
  
# This module is imported so that we can 
# play the converted audio
import os
  
# The text that you want to convert to audio
mytext = "In 2011, ten women in Bilbao, Spain, got together to publicly proclaim their self-love and marry themselves. It started out as a fun, rebellious act against traditional marriage, but in fact, they were tapping into something already underway globally. It's called sologamy."
  
# Language in which you want to convert
language = 'en'
tld = 'com.au'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False, tld=tld)
  
# Saving the converted audio in a mp3 file named
# welcome 
myobj.save("test.mp3")
  
# Playing the converted file
os.system("test.mp3")

## Book to mp3
page = df['page'][12]
language = 'en'
tld = 'co.in'
myobj = gTTS(text=content, lang=language, slow=False, tld=tld)
myobj.save("book.mp3")
os.system("book.mp3")
# Sandbox
test = "Hey, dirty girl"

language = 'en'
tld = 'co.in'
myobj = gTTS(text=test, lang=language, slow=False, tld=tld)
myobj.save("test.mp3")
os.system("test.mp3")
import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

def hello ():  
    label1 = tk.Label(root, text= 'Hello World!', fg='black', font=('Brill', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)
    
button1 = tk.Button(text='Yo', command=hello, bg='gray',fg='white', font=('Brill', 12))
canvas1.create_window(150, 150, window=button1)

root.mainloop()
