# read-aloud

This is a rudimentary attempt to create a simple PDF reader using free and open source components. By "reader" I mean reading aloud using a text-to-speech engine.

## Prerequisites

You will need *PyPDF2*, a PDF to text converter and *pyttsx3*, a text-to-speach engine.

    `pip install pyttsx3`

    `pip install PyPDF2`

## Instructions

Download `main.py`, place a pdf next to it, and run `main.py`. 

The terminal will ask you five questions about the voice and speed preference, the path and the filename, and whether you want to continue on a specific page. You can just hit enter to each prompt to choose the defaults (will choose first pdf alphabetically in the current folder). I have no way of pausing or stopping the reader at the moment. This project took me half day.
