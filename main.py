print("\n###########################################################\n### Initiating Parti Gábor's Primitive PDF Audio Reader ###\n###########################################################\n")
  
print("Instructions:\n - Put a pdf in the same folder as this python file.\n - A quick setup will follow with 5 options: voice, speed, path, document, and page; you have to input your settings.\n - Press enter for the default settings.\n\nDependencies: You will also need these two packages: PyPDF2, pyttsx3.")

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
path = sys.path[0]
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