print("\n###############################################\n### Initiating Parti's Primitive PDF Reader ###\n###############################################\n")

print("Same, like main.py but using Google's TTS engine to convert text to audio. Needs an active internet connection.")
# %pip install pyttsx3
# %pip install PyPDF2
# %pip install pygame # not needed

import os
import sys
import glob
import pandas as pd
import numpy as np
import regex as re
import time
import PyPDF2
import pyttsx3
from gtts import gTTS
# from pygame import mixer # not needed

## Use auto-py-to-exe to make exe ##

### Setup

# engine
language = 'en'
tld = 'com.au'

# paths
# relative path (current folder)
path = sys.path[0]

# list of pdfs in relative  directory
pdfs = glob.glob("*.pdf")

# file
book_choice = pdfs[0]

# select file
print("\nPlease select a pdf. Enter the filename here, with extension. (Hit enter for the first pdf alphabetically)")
book_choice = str(input("Please enter filename: ")) or book_choice

### Parsing

# creating a pdf file object
pdfFileObj = open(path+"\\"+book_choice, 'rb')

print("\tParsing book:", path+"\\"+book_choice,"\n\tThis might take some time if your document is several hundred pages long...")

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

print("\tPages found:", df.shape[0])
df['page'].replace('', np.nan, inplace=True)
df.dropna(subset=['page'], inplace=True)
df.reset_index(drop=True, inplace=True)

# printing number of pages in pdf file 
print("\tDropping empty ones... Done\n\tTotal number of pages: ", str(df.shape[0]))
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

# estimate
word_counts = df["page"].apply(lambda n: len(n.split()))
minutes = word_counts.sum() / 140 #estimate
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

# Play
for i, row in df.iterrows():
    print("\n=== PAGE #", str(i), " ===")
    print(row['page'])
    myobj = gTTS(text=row['page'], lang=language, slow=False, tld=tld)
    # myobj.save("page"+ str(i) +".mp3")
    print("Recording...")
    myobj.save("page.mp3")
    print("Page saved.")
    os.system("page.mp3")

print("Book finished!")