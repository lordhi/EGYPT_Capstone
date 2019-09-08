import tkinter as tk
general_background = '#ffffff'
class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 200
        y += self.widget.winfo_rooty() + 5    
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        print("entered")
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background=general_background, relief='solid', borderwidth=1,
                       font=("times", "10", "normal"))
        label.pack(ipadx=1)
 
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()