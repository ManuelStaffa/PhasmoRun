import sys, os
import pydirectinput
from tkinter import *
import pywintypes, win32gui
from win32gui import GetWindowText, GetForegroundWindow
from pynput.keyboard import Listener, Key, KeyCode
from configparser import ConfigParser
from sys import exit
from dict import keyDictionary


# Initialize -------------------------------------------------------------------
def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return f'{os.path.join(sys._MEIPASS, filename)}'
    else:
        return f'{filename}'


# Read file
def readFile(search):
    dir_path = '%s\\PhasmoRun\\' %  os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = '%sconfig.ini' % dir_path

    try:
        config.read(file_path)
        return config.get("settings", search)
    except:
        editLabel("No save found")
        writeFile("autorun_key", keyDictionary["Key.f1"])


# Write file
def writeFile(name, value):
    dir_path = '%s\\PhasmoRun\\' %  os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = '%sconfig.ini' % dir_path

    try:
        config.set("settings", str(name), str(value))
        with open(file_path, 'w') as configfile:
            config.write(configfile)
        editLabel("Saved key config")
    except:
        config.add_section("settings")
        config.set("settings", "autorun_key", "Key.f1")
        with open(file_path, 'w') as configfile:
            config.write(configfile)


"""keyDictionary = {
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
    "Key.scroll_lock":Key.scroll_lock}"""


# Variables --------------------------------------------------------------------
config = ConfigParser()

global autorun
global rebind
global autorunKey
autorun = False
rebind = False

try:
    key = readFile("autorun_key")
    if len(key) == 1:
        autorunKey = KeyCode.from_char(key)
    else:
        autorunKey = keyDictionary[key]
except:
    autorunKey = keyDictionary["Key.f1"]

version = "2.2.0"
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
window.iconbitmap(get_path("phasmo.ico"))


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
            disableAutorun()
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
    editLabel("Disabled auto sprint.")

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
                        text="Click to change keybind.\nCurrent key: {}".format(str(autorunKey).replace("'", "")))


# Disables the rebind button
def disableKeybind():
    global rebind
    global autorunKey

    rebind = False
    buttonKeybind.configure(bg=blue,
                    activebackground=blue,
                    text="Click to change keybind.\nCurrent key: {}".format(str(autorunKey).replace("'", "")))


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
        writeFile("autorun_key", str(autorunKey).replace("'", ""))
        editLabel("Key bound to {}".format(str(autorunKey).replace("'", "")))
        info.configure(text="Press [{}] to start, and [f4] to force quit".format(str(autorunKey).replace("'", "")))
        disableKeybind()


# Window contents --------------------------------------------------------------
info = Label(text="Press [{}] to start, and [f4] to force quit".format(str(autorunKey).replace("'", "")),
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
                    disabledforeground=white,
                    activeforeground=white,
                    bd=0,
                    state="disabled",
                    command=toggleAutorun)

buttonKeybind = Button(text="Click to change keybind.\nCurrent key: {}".format(str(autorunKey).replace("'", "")),
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
window.protocol("WM_DELETE_WINDOW", endProgram)
window.mainloop()
a=input("a")
