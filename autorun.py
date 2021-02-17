import time
import pyautogui
import pydirectinput
from win32gui import GetWindowText, GetForegroundWindow
from pynput import keyboard
from pynput.keyboard import Key, Listener
from sys import exit
import tkinter as tk

#pip install pyautogui
#pip install pydirectinput
#pip install pynput
#pip install win32gui

#print("Press [f1] to start, and [f4] to force quit")
shift_hold = False
status = "not running"
window = tk.Tk()
window.title("Phasmophobia Autorun")

def keyPress(key):
    global shift_hold
    global status

    if key == keyboard.Key.f4:
        status = "Disabled auto sprint - Stopping script..."
        shift_hold = False
        pydirectinput.keyUp('shiftleft')
        pydirectinput.keyUp('shiftright')
        window.destroy()
        exit()

    if key == keyboard.Key.tab or key == keyboard.Key.cmd:
        status = "Disabled auto sprint - Tabbed out of game."
        shift_hold = False
        pydirectinput.keyUp('shiftleft')
        pydirectinput.keyUp('shiftright')

    if key == keyboard.Key.f1 and (GetWindowText(GetForegroundWindow()) == "Phasmophobia"):

        shift_hold = not shift_hold
        if(shift_hold):
            status = "Enabled auto sprint."
            try:
                pydirectinput.keyDown('shiftleft')
                pydirectinput.keyDown('shiftright')
            except:
                status = "Uh Oh. Something went wrong."
                exit()
        else:
            status = "Disabled auto sprint."
            try:
                pydirectinput.keyUp('shiftleft')
                pydirectinput.keyUp('shiftright')
            except:
                status = "Uh Oh. Something went wrong."
                exit()

    if key == keyboard.Key.f1 and not (GetWindowText(GetForegroundWindow()) == "Phasmophobia"):
        status = "Please start/focus Phasmophobia."

    if key == keyboard.Key.f1 or key == keyboard.Key.f4 or key == keyboard.Key.tab or key == keyboard.Key.cmd:
        text_box.insert("1.0","\n"+status)



listener = Listener(on_press=keyPress)
listener.start()

message = tk.Label(text="Press [f1] to start, and [f4] to force quit")
message.pack()
text_box = tk.Text()
text_box.pack()
window.mainloop()
