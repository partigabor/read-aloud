print("\n###############################################\n### Initiating Parti's Primitive PDF Reader ###\n###############################################\n")

print("Instructions:\n - Put a pdf in the same folder as this python file.\n\nDependencies: You will also need some python packages, run `pip install -r requirements.txt`.\nLimitations: Currently the only way to stop the engine is to kill the terminal.")

# %pip install pyttsx3
# %pip install PyPDF2

import os
import sys
import glob
import pandas as pd
import numpy as np
import regex as re
import time
import PyPDF2
import pyttsx3

### Use auto-py-to-exe to make exe ###

# setup engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# voice
engine.setProperty('voice', voices[1].id)

# speed
engine.setProperty('rate', 200)

# relative path (current folder)
path = sys.path[0] # does not work with auto-py-to-exe, use "C:\\Users\\user\\...\\"

# list of pdfs in relative  directory
pdfs = glob.glob("*.pdf")

# list of pdfs in absolute directory
# pdfs = []
# os.chdir(path)
# for file in glob.glob("*.pdf"):
#     pdfs.append(file)

# file
book_choice = pdfs[0]

### Parsing ###

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

print("\tPages found:",df.shape[0])
df['page'].replace('', np.nan, inplace=True)
df.dropna(subset=['page'], inplace=True)
df.reset_index(drop=True, inplace=True)

# printing number of pages in pdf file 
print("\tDropping empty ones... Done\n\tTotal number of pages are", str(df.shape[0]))
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

# print("\nEnter the page number you would like to continue, or hit enter to start from the beginning.")
# page_choice = input("Please enter page number: ") or "0"
# page_choice = int(page_choice)
# print("\tPage", str(page_choice), "selected, flipping to the page now...")
# time.sleep(1)

# # cutoff before start
# df = df.iloc[page_choice: , :]

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

#play
for i, row in df.iterrows():
    print("\n# PAGE NO.", str(i), "#")
    print(row['page'])
    engine.say(row['page']) # to read immediately
    engine.runAndWait()

print("Book finished!")