ruler = "\n###############################################\n"
print(ruler + "### Initiating Parti's Primitive PDF Reader ###" + ruler)


# %pip install pyttsx3
# %pip install PyPDF2
# %pip install pygame # not needed

# import easygui # not needed
import os
import sys
import glob
import pandas as pd
import numpy as np

import re

import time
import PyPDF2
import pyttsx3

from read_aloud_utils import textfilter

# Choose a language
from read_aloud_utils import localized
locales = localized()


print(locales.get("Introduction"))
#
current_language_name = locales.current_language_name


# from pygame import mixer # not needed

### Use auto-py-to-exe to make exe ###

# setup engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#for voice in voices:
#  print(voice)

# voice
# engine.setProperty('voice', voices[1].id)

# select voice
print(locales.get("SelectVoice"))
voice_choice = str(input(locales.get("QuestionVoiceChoice"))) or "f"

if voice_choice == "m":
  engine.setProperty('voice', voices[0].id)
  print(locales.get("AnswerFirstVoiceSelected"))
  #
elif voice_choice == "f": 
  engine.setProperty('voice', voices[1].id)
  print(locales.get("AnswerSecondVoiceSelected"))
  #
elif voice_choice == "s":
  for voice in voices:
    if locales.current_lang in voice.languages or current_language_name in voice.name:
      engine.setProperty('voice', voice.id)
      break
else:
  engine.setProperty('voice', voices[1].id)
  print(locales.get("OopsNotAnyRightKey"))
  exit()



# speed
# engine.setProperty('rate', 200)

# select speed
print(locales.get("SelectSpeed"))
speed_choice = input(locales.get("QuestionEnterSpeed")) or "200"
engine.setProperty('rate', int(speed_choice))
print(locales.get("AnswerSpeedSelected").format(speed_choice))



### Paths ###

# relative path (current folder)
# path = sys.path[0] # does not work with auto-py-to-exe

# absolute path (local)
print(locales.get("SelectDirectory"))
path = sys.path[0] # does not work with auto-py-to-exe
#
path_choice = input(locales.get("QuestionEnterPath")) or path
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
print(locales.get("SelectPDFFile"))
book_choice = str(input(locales.get("QuestionSelectPDF"))) or pdfs[0]



### Parsing ###

# creating a pdf file object
pdfFileObj = open(path+"\\"+book_choice, 'rb')

print(locales.get("ParsingBook") + path+"\\"+book_choice)
#
print(locales.get("HavePatience"))

# initialize dataframe to hold documents
df = pd.DataFrame(columns=['page_no', 'page'])

print("\t1/3...")

# creating a pdf reader object 
reader = PyPDF2.PdfReader(pdfFileObj, strict=False) 
pages = len(reader.pages)
#
#print(locales.get("InfoNumPages").format(pages))
#possible early user interaction here

print("\t2/3...")

for p in range(pages):
  pageObj = reader.pages[p]
  # print(p)
  df.loc[p, 'page_no'] = p+1
  page_content = pageObj.extract_text()
  # print(page_content)
  df.loc[p, 'page'] = page_content

print("\t3/3...")

#closing the pdf file object 
pdfFileObj.close() 

print(locales.get("InfoNumPages").format(df.shape[0]))
df['page'].replace('', np.nan, inplace=True)
df.dropna(subset=['page'], inplace=True)
df.reset_index(drop=True, inplace=True)

# printing number of pages in pdf file 
print(locales.get("DroppingEmptyPages"), str(df.shape[0]))
time.sleep(1)
print(locales.get("TidyingUp"))

df['page'] = textfilter.make_readable(df['page'])

content = " ".join(df['page'].tolist())

print(locales.get("SelectStartingPage"))
page_choice = input(locales.get("QuestionStartPage")) or "0"

page_choice = int(page_choice)
print(locales.get("FlippingPage").format(page_choice))
time.sleep(1)

# cutoff before start
df = df.iloc[page_choice: , :]

# estimate
word_counts = df["page"].apply(lambda n: len(n.split()))
minutes = word_counts.sum() / int(speed_choice) #estimate
seconds = minutes* 60

def convert_to_preferred_format(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60
   return "%02d:%02d:%02d" % (hour, min, sec) 

print(locales.get("EstimatedAudioTime"), convert_to_preferred_format(seconds))
time.sleep(1)

# print("\nGo!\n")
# df.head(20)

#play
for i, row in df.iterrows():
    print("\n# PAGE NO.", str(i), "#")
    print(row['page'])
    engine.say(row['page']) # to read immediately
    engine.runAndWait()
print(ruler)
print(locales.get("BookFinished"))