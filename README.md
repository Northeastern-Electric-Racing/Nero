# NERO

## Getting Started

This section will take you through setting up the project, running the project, then learning about the libraries we use for the GUI.

### Setting up the project

Installing Python:

1. https://www.python.org/downloads/
2. you're done when you can run `python3` in your terminal and it works
3. make sure you have the most recent version

Installing Git Submodule

1. `git submodule update --init`

Installing dependencies:

installing Python should come with pip3, so in your terminal you can do:

1. `pip3 install venv` <-- (only do if you haven't installed venv already)
2. `virtualenv venv` <-- (only do if the venv folder doesn't exist already)
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`

### Running the project

You can click the play button in VSCode when you're in the `main.py` file or you can do:

1. `source venv/bin/activate`
2. `python3 main.py`

### Dev Inputs 
   Increment Mode -> Right Arrow
   Decrement Mode -> Left Arrow
   Increment Page -> Right Shift
   Debug Mode -> Left Shift
   Up -> Up Arrow
   Down -> Down Arrow
   Enter -> Enter Key

Notes:
- Enter on the plot page changes the time frame
- Press up and down on the debug table to move between values, press enter to select one for plotting
- You may have to brew install python-tk if on mac or linux if you get a _tkinter module not found error
- You may have to install requirements on your machine if virtualenv is not working

### Learning

We use CustomTkinter which is a more modern version of Tkinter. 

The link to the repo is here: https://github.com/TomSchimansky/CustomTkinter

Their docs are here and are very good: https://github.com/TomSchimansky/CustomTkinter/wiki

It is all based on Tkinter, so if these docs don't explain it then the Tkinter docs will somewhere.

### Installing New Dependencies

1. `source venv/bin/activate`
2. `pip3 install NEW_DEPENDENCY`
3. `pip3 freeze > requirements.txt`

Then commit the new requirements.txt which should have added lines for the new package you're installing and any of its dependencies.

