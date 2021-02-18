"""
Keep-Alive.py
This file is part of Keep-Alive

Copyright (C) 2021 - Vishnu Pradeesh Lekshmanan

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""


import pyautogui
import tkinter as tk
from threading import *
import datetime
from configparser import ConfigParser
from time import sleep
from os import path
import webbrowser

config_object = ConfigParser()

if path.exists("config.ini"):
    pass
else:
    config_object["Windows"] = {
        "WINX": 360,
        "WINY": 140,
        "BACKGROUND": "light green",
        "FONT": "helvetica",
        "FONTSIZE": 12,
        "SLEEPTIME": 30
    }
    with open("config.ini", "w") as conf:
        config_object.write(conf)

# Read config.ini file
config_object.read("config.ini")

lock = Lock()

class Application(tk.Tk):
    windowSettings = config_object["Windows"]
    sx, sy = int(windowSettings["WINX"]), int(windowSettings["WINY"])
    geo = str(sx) + "x" + str(sy)
    condition = True
    fontFace = windowSettings["FONT"]
    fontSize = int(windowSettings["FONTSIZE"])
    background = windowSettings["BACKGROUND"]
    sleepTime = int(windowSettings["SLEEPTIME"])

    def __init__(self):
        tk.Tk.__init__(self)
        self.create_window()
        self.create_label()
        self.GitLink()
        self.frame = tk.Frame(self)
        self.frame.config(bg="white")
        self.frame.pack(side="bottom", padx=10, pady=10)
        self.create_button()
        self.create_note()
        self.pack()

    def loop(self):
        self.mainloop()

    def create_window(self):
        # Windows dimension
        # self.iconbitmap("icon.ico")
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file="icon.png"))
        self.title("Keep Alive")
        self.config(bg=self.background)
        self.geometry(self.geo)

    def create_label(self):
        self.label = tk.Label(
            self,
            text="Start to keep alive",
            wraplength=int(self.sx-10),
            justify="center",
            bg=self.background
        )
        self.label.config(font=(self.fontFace, self.fontSize, "bold"))
    
    def create_note(self):
        self.note = tk.Label(
            self.frame,
            text=f"Note: Once started, the app shifts volume up & down by {self.sleepTime} seconds.\nChange settings in config.ini",
            wraplength=int(self.sx*0.7),
            justify="left",
            fg="red"
        )
        self.note.config(font=("helvetica", 9))

    def callback(self, url):
        webbrowser.open_new_tab(url)
    
    def GitLink(self):
        self.GitLink = tk.Label(
            self,
            text="Fork Me On GitHub",
            wraplength=int(self.sx*0.8),
            justify="left",
            bg=self.background,
            fg="blue",
            cursor="hand2"
        )
        self.GitLink.config(font=("helvetica", 8))
        self.GitLink.bind("<Button-1>", lambda e: callback("https://github.com/matriculus/Keep-Alive"))
    
    def create_button(self):
        self.button = tk.Button(
            self.frame,
            text="Start",
            bd="1",
            command=self.start_thread,
            font=self.fontFace,
            bg="#91dbde",
            activebackground="#f47983"
        )

    def pack(self):
        self.label.pack(padx=2, pady=2)
        self.GitLink.pack(side="bottom", padx=2, pady=2)
        subFrame = tk.Frame(self)
        subFrame.pack(side="bottom")
        self.button.pack(side="right", pady=10, padx=10)
        self.note.pack(side="left", padx=2, pady=2)

    def stop_alive(self):
        lock.acquire()
        self.condition = False
        lock.release()
        self.appthread.join()
        self.condition = True
        self.button.config(text="Start", command=self.start_thread)

    def start_alive(self):
        self.button.config(text="Stop", command=self.stop_alive)
        lastTime = datetime.datetime.now()
        flag = True
        lock.acquire()
        cond = self.condition
        lock.release()
        while cond:
            period = datetime.datetime.now()
            lock.acquire()
            cond = self.condition
            lock.release()
            if (period - lastTime).total_seconds() >= self.sleepTime:
                if flag:
                    pyautogui.press("Volumeup")
                    flag = False
                else:
                    pyautogui.press("Volumedown")
                    flag = True
                lastTime = period
            sleep(0.2)

    def start_thread(self):
        self.appthread = Thread(target=self.start_alive)
        self.appthread.start()


def main():
    app = Application()
    app.loop()
    return 0


if __name__ == "__main__":
    main()
