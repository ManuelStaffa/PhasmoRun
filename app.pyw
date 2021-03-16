from tkinter import *
import pydirectinput
import win32process, win32gui, win32con
import pywintypes
from win32gui import GetWindowText, GetForegroundWindow
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
from sys import exit
import sys, os


# Initialize -------------------------------------------------------------------
# Read file
def readFile(search):
    try:
        with open("test.txt", "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.endswith("\n"):
                    lines[i] = line[:-1]

            for line in lines:
                if line.startswith(search):
                    return line[len(search)+1:].strip()
    except:
        with open("test.txt", "w") as file:
            file.write("autorunKey=Key.alt_l")


# Key dictionary
keyDictionary = {
    "Key.alt":Key.alt,
    "Key.alt_l":Key.alt_l,
    "Key.alt_r":Key.alt_r,
    "Key.alt_gr":Key.alt_gr,
    "Key.backspace":Key.backspace,
    "Key.caps_lock":Key.caps_lock,
    "Key.cmd":Key.cmd,
    "Key.cmd_l":Key.cmd_l,
    "Key.cmd_r":Key.cmd_r,
    "Key.ctrl":Key.ctrl,
    "Key.ctrl_l":Key.ctrl_l,
    "Key.ctrl_r":Key.ctrl_r,
    "Key.delete":Key.delete,
    "Key.down":Key.down,
    "Key.end":Key.end,
    "Key.enter":Key.enter,
    "Key.esc":Key.esc,
    "Key.f1":Key.f1,
    "Key.f2":Key.f2,
    "Key.f3":Key.f3,
    "Key.f4":Key.f4,
    "Key.f5":Key.f5,
    "Key.f6":Key.f6,
    "Key.f7":Key.f7,
    "Key.f8":Key.f8,
    "Key.f9":Key.f9,
    "Key.f10":Key.f10,
    "Key.f11":Key.f11,
    "Key.f12":Key.f12,
    "Key.f13":Key.f13,
    "Key.f14":Key.f14,
    "Key.f15":Key.f15,
    "Key.f16":Key.f16,
    "Key.f17":Key.f17,
    "Key.f18":Key.f18,
    "Key.f19":Key.f19,
    "Key.f20":Key.f20,
    "Key.home":Key.home,
    "Key.left":Key.left,
    "Key.page_down":Key.page_down,
    "Key.page_up":Key.page_up,
    "Key.right":Key.right,
    "Key.shift":Key.shift,
    "Key.shift_l":Key.shift_l,
    "Key.shift_r":Key.shift_r,
    "Key.space":Key.space,
    "Key.tab":Key.tab,
    "Key.up":Key.up,
    "Key.media_play_pause":Key.media_play_pause,
    "Key.media_volume_mute":Key.media_volume_mute,
    "Key.media_volume_down":Key.media_volume_down,
    "Key.media_volume_up":Key.media_volume_up,
    "Key.media_previous":Key.media_previous,
    "Key.media_next":Key.media_next,
    "Key.insert":Key.insert,
    "Key.menu":Key.menu,
    "Key.num_lock":Key.num_lock,
    "Key.pause":Key.pause,
    "Key.print_screen":Key.print_screen,
    "Key.scroll_lock":Key.scroll_lock}


# Variables --------------------------------------------------------------------
global autorun
global rebind
global autorunKey
autorun = False
rebind = False
try:
    if len(readFile("autorunKey")) == 1:
        autorunKey = KeyCode.from_char(readFile("autorunKey"))
    else:
        autorunKey = keyDictionary[readFile("autorunKey")]
except:
    autorunKey = Key.alt_l

version = "2.0.1"
window_width = "300"
window_height = "300"

green = "#98971a"
red = "#cc241d"
grey = "#202020"
white = "#fbf1c7"
blue = "#458588"
lightblue = "#83a598"


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
    autorun = not autorun

    if autorun:
        #buttonAutorun.select()
        buttonAutorun.configure(background=green,
                        activebackground=green)
        if GetWindowText(GetForegroundWindow()) == "Phasmophobia":
            try:
                pydirectinput.keyDown('shiftleft')
                pydirectinput.keyDown('shiftright')
            except:
                editLabel("Uh Oh. Something went wrong.")
                endProgram()
        else:
            editLabel("Please start/focus Phasmophobia.")

    else:
        #buttonAutorun.deselect()
        buttonAutorun.configure(bg=red,
                        activebackground=red)
        try:
            pydirectinput.keyUp('shiftleft')
            pydirectinput.keyUp('shiftright')
        except:
            editLabel("Uh Oh. Something went wrong.")
            endProgram()


# Disable Autorun
def disableAutorun():
    global autorun
    autorun = False

    #buttonAutorun.deselect()
    buttonAutorun.configure(bg=red,
                    activebackground=red)
    editLabel("Disabled auto sprint - tabbed out of game.")

    try:
        pydirectinput.keyUp('shiftleft')
        pydirectinput.keyUp('shiftright')
    except:
        editLabel("Uh Oh. Something went wrong.")
        endProgram()


# Rebind autorun key
def keybind():
    global rebind
    rebind = not rebind

    if rebind:
        buttonKeybind.configure(background=lightblue,
                        activebackground=lightblue,
                        text="Press any key to rebind.")
    else:
        #buttonAutorun.deselect()
        buttonKeybind.configure(bg=blue,
                        activebackground=blue,
                        text="Click to change keybind.\nCurrent key: {}".format(autorunKey))


# Disables the rebind button
def disableKeybind():
    global rebind
    global autorunKey

    rebind = False
    buttonKeybind.configure(bg=blue,
                    activebackground=blue,
                    text="Click to change keybind.\nCurrent key: {}".format(autorunKey))


# Edit Label
def editLabel(status):
    text_len = len(text_box.cget("text").rstrip().split("\n"))
    if text_len > 8:
        text = "\n".join(text_box.cget("text").rstrip().split("\n")[1:])
        text_box.configure(text="{}\n{}".format(text, status))
    else:
        text_box.configure(text="{}\n{}".format(text_box.cget("text").rstrip(), status))


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
    global rebind
    global autorunKey

    # Toggle autorun
    if key == autorunKey:
        toggleAutorun()

    # End program
    if key == Key.f4:
        endProgram()

    # Pause when tabbed out
    if key == Key.tab or key == Key.cmd:
        disableAutorun()

    # Rebind key
    if rebind:
        autorunKey = key
        editLabel("Key bound to {}".format(autorunKey))
        with open("test.txt", "w") as file:
            if str(autorunKey).startswith("'"):
                writeKey = str(autorunKey)[1:-1]
            else:
                writeKey = autorunKey
            file.write("autorunKey={}".format(writeKey))
        info.configure(text="Press [{}] to start, and [f4] to force quit".format(autorunKey))
        disableKeybind()


# Window contents --------------------------------------------------------------
info = Label(text="Press [{}] to start, and [f4] to force quit".format(autorunKey),
                width=window_width,
                height="3",
                background=grey,
                foreground=white)

#state = BooleanVar()
buttonAutorun = Button(text="Enable/disable autorun",
                    width=window_width,
                    height="3",
                    #selectcolor=grey,
                    background=red,
                    activebackground=red,
                    foreground=white,
                    activeforeground=white,
                    bd=0,
                    command=toggleAutorun)

buttonKeybind = Button(text="Click to change keybind.\nCurrent key: {}".format(str(autorunKey)),
                    width=window_width,
                    height="3",
                    #selectcolor=grey,
                    background=blue,
                    activebackground=blue,
                    foreground=white,
                    activeforeground=white,
                    bd=0,
                    command=keybind)

text_box = Label(text="Status messages will appear here",
                width=window_width,
                #height="3",
                #state=DISABLED,
                background=grey,
                foreground=white)


# Pack all contents to window --------------------------------------------------
info.pack()
#info.grid(column=0, row=0)
buttonAutorun.pack()
buttonKeybind.pack()
text_box.pack()


# Run program ------------------------------------------------------------------
listener = Listener(on_press=keyPress)
listener.start()
window.mainloop()
