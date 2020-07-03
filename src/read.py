import tkinter as tk
import tkinter.simpledialog

class Read():
    def __init__(self, init = 0):
        self.init = init
    
    def buscar(self, title):
        win = tk.Tk()
        win.withdraw()
        win.geometry('100x200')
        win.title("Augus: find Replace")

        word = tk.simpledialog.askstring("title",title)
        return word
        win.mainloop()