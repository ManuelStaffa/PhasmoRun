from tkinter import *
import pydirectinput
from win32gui import GetWindowText, GetForegroundWindow
from pynput import keyboard
from pynput.keyboard import Listener
from sys import exit
import sys, os


# Variables --------------------------------------------------------------------
global autorun
autorun = False
global status
status = ""

version = "2.0.1"
window_width = "300"
window_height = "300"

green = "#98971a"
red = "#cc241d"
grey = "#202020"
white = "#fbf1c7"


# Window settings --------------------------------------------------------------
window = Tk()
window.title("PhasmoRun {}".format(version))
window.geometry("{}x{}".format(window_width, window_height))
window.configure(bg=grey)
#window.iconbitmap("phasmo.ico")


# Functions --------------------------------------------------------------------
# Toggle autorun
def toggleAutorun():
    global autorun
    global status
    autorun = not autorun

    if autorun:
        checkAutorun.select()
        checkAutorun.configure(background=green,
                        activebackground=green)
        if GetWindowText(GetForegroundWindow()) == "Phasmophobia":
            try:
                pydirectinput.keyDown('shiftleft')
                pydirectinput.keyDown('shiftright')
            except:
                status = "Uh Oh. Something went wrong."
                endProgram()
        else:
            status = "Please start/focus Phasmophobia."

    else:
        checkAutorun.deselect()
        checkAutorun.configure(bg=red,
                        activebackground=red)
        try:
            pydirectinput.keyUp('shiftleft')
            pydirectinput.keyUp('shiftright')
        except:
            status = "Uh Oh. Something went wrong."
            endProgram()

    text_box.insert("1.0",status+"\n")


# Disable Autorun
def disableAutorun():
    global autorun
    autorun = False

    checkAutorun.deselect()
    checkAutorun.configure(bg=red,
                    activebackground=red)
    status = "Disabled auto sprint - tabbed out of game."

    try:
        pydirectinput.keyUp('shiftleft')
        pydirectinput.keyUp('shiftright')
    except:
        status = "Uh Oh. Something went wrong."
        endProgram()

    text_box.insert("1.0",status+"\n")


# End program
def endProgram():
    #status = "Disabled auto sprint - Stopping script..."
    pydirectinput.keyUp('shiftleft')
    pydirectinput.keyUp('shiftright')
    window.destroy()
    exit()


# Key press
def keyPress(key):
    global autorun
    global status

    # Toggle autorun
    if key == keyboard.Key.f1:
        toggleAutorun()

    # End program
    if key == keyboard.Key.f4:
        endProgram()

    # Pause when tabbed out
    if key == keyboard.Key.tab or key == keyboard.Key.cmd:
        disableAutorun()


# Window contents --------------------------------------------------------------
info = Label(text="Press [f1] to start, and [f4] to force quit",
                width = window_width,
                height="3",
                background=grey,
                foreground=white)

state = BooleanVar()
checkAutorun = Checkbutton(text='Enable/disable autorun',
                    width = window_width,
                    height="3",
                    selectcolor=grey,
                    background=red,
                    activebackground=red,
                    foreground=white,
                    activeforeground=white,
                    command=toggleAutorun)

text_box = Text(width = window_width,
                #height="3",
                #state=DISABLED,
                background=grey,
                foreground=white)


# Pack all contents to window --------------------------------------------------
info.pack()
#info.grid(column=0, row=0)
checkAutorun.pack()
text_box.pack()


# Run program ------------------------------------------------------------------
listener = Listener(on_press=keyPress)
listener.start()
window.mainloop()
