ruler = "\n###############################################\n"
print(ruler + "### Initiating Parti's Primitive PDF Reader ###" + ruler)

# %pip install pyttsx3
# %pip install PyPDF2

import os
import sys
import glob
import pandas as pd
import numpy as np

import re
import json

import time
import PyPDF2
import pyttsx3

# Switch to default UI's language if possible
import locale
import ctypes
windll = ctypes.windll.kernel32
current_lang = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]
langdic = {\
  "en_GB" : "English (Great Britain)",\
  "en_US" : "English (United States)",\
  "de_DE" : "German"\
}

json_data = ""

try:
  with open(f"locales/{current_lang}.json") as jsd:
    json_data = json.load(jsd)
  jsd.close()
except:
  with open(f"locales/default.json") as jsd:
    json_data = json.load(jsd)
  jsd.close()

#for testing 
#current_language_name = "English (United States)"
#
try:
  current_language_name = langdic[current_lang]
except:
  current_language_name = "English (United States)"

### Use auto-py-to-exe to make exe ###

# setup engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# voice
#engine.setProperty('voice', voices[1].id)
for voice in voices:
  if current_lang in voice.languages or current_language_name in voice.name:
    engine.setProperty('voice', voice.id)
    break

# speed
engine.setProperty('rate', 200)

# relative path (current folder)
path = sys.path[0] # does not work with auto-py-to-exe, use "C:\\Users\\user\\...\\"

# list of pdfs in absolute directory
pdfs = []
os.chdir(path)
for file in glob.glob("*.pdf"):
    pdfs.append(file)

# file
book_choice = pdfs[0]

### Parsing ###

# creating a pdf file object
pdfFileObj = open(path+"\\"+book_choice, 'rb')

print(json_data["ParsingBook"] + path+"\\"+book_choice)
#
print(json_data["HavePatience"])

# initialize dataframe to hold documents
df = pd.DataFrame(columns=['page_no', 'page'])

# creating a pdf reader object 
reader = PyPDF2.PdfReader(pdfFileObj, strict=False) 
pages = len(reader.pages)

for p in range(pages):
  pageObj = reader.pages[p]
  # print(p)
  df.loc[p, 'page_no'] = p+1
  page_content = pageObj.extract_text()
  # print(page_content)
  df.loc[p, 'page'] = page_content

#closing the pdf file object 
pdfFileObj.close() 

print(json_data["InfoNumPages"].format(df.shape[0]))
df['page'].replace('', np.nan, inplace=True)
df.dropna(subset=['page'], inplace=True)
df.reset_index(drop=True, inplace=True)

# printing number of pages in pdf file 
print(json_data["DroppingEmptyPages"], str(df.shape[0]))
time.sleep(1)
print(json_data["TidyingUp"])

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

print(json_data["EstimatedAudioTime"], convert_to_preferred_format(seconds))
time.sleep(1)

#play
for i, row in df.iterrows():
    print("\n# PAGE NO.", str(i), "#")
    print(row['page'])
    engine.say(row['page']) # to read immediately
    engine.runAndWait()
print(ruler)
print(json_data["BookFinished"])