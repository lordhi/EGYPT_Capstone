from tkinter import *
import time

master = Tk()

def callback():
    print("click!")

b = Button(master, text="OK", command=callback)
b.pack()

while 1:
	master.update_idletasks()
	master.update()
	time.sleep(0.1)