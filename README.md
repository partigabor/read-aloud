# read-aloud

This is a rudimentary attempt to create a simple PDF reader using free and open source components. By "reader" I mean reading aloud using a text-to-speech engine (TTS).

## Instructions

### 1. Installation

Install requirements, you will need *PyPDF2*, a PDF to text converter and *pyttsx3*, a text-to-speach engine (among a few other basic data management packages).

    pip install -r requirements.txt

### 2. Run `reader.py`. 

The terminal will ask you five questions about the voice and speed preference, the path and the filename, and whether you want to continue on a specific page. You can just hit enter at each prompt to choose the defaults (will choose first pdf alphabetically in the current folder). I have no way of pausing or stopping the reader at the moment, this was made for fun in the course of one Saturday.

Use `reader-express.py` to skip all options and just start reading the first pdf in the same directory as the python file.
