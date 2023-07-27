# read-aloud

This is a rudimentary attempt to create a simple PDF reader using free and open source components. By "reader" I mean reading aloud using a text-to-speech engine (TTS).

## Instructions

### 1. Installation

Install requirements, you will need *PyPDF2*, a PDF to text converter and *pyttsx3*, a text-to-speach engine (among a few other basic data management packages).

    pip install -r requirements.txt

### 2. Download and run `reader.py`. 

The terminal will ask you five questions about the voice and speed preference, the path and the filename, and whether you want to continue on a specific page. You can just hit enter to each prompt to choose the defaults (will choose first pdf alphabetically in the current folder). I have no way of pausing or stopping the reader at the moment.

Use `reader-express.py` to skip all options and just start reading the first pdf next to the python file.
