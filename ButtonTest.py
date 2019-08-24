from tkinter import *
import time

def button_pause_on_click():
	print("Hello")
	print("There")
	sys.exit()


tk = Tk()

button_pause = Button(tk,text='Pause',command = button_pause_on_click)
button_pause.grid(row=0,column=2,padx=5,pady=5)

tk.mainloop()

while 1:
	tk.update_idletasks()
	tk.update()
	time.sleep(0/1)