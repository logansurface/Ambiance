from tkinter import *
from tkinter import ttk

class MainWindow:
    def __init__(self, title: str):
        self.root = Tk()
        self.root.title(title)
        self.__add_frame()
        self.__add_canvas()
        self.__add_buttons()

    def __add_frame(self, pad=3): 
        self.root_frame = ttk.Frame(self.root, padding=pad)
        self.root_frame.grid(sticky=(N, S, E, W))
        
    def __add_canvas(self, x=640, y=480):
        self.display = Canvas(self.root_frame, width=x, height=y, background='gray75')
        self.display.grid(column=1, row=1 , sticky=(N, S, E, W))
    
    def __add_buttons(self):
        self.pause_btn = ttk.Button(self.root_frame, text="Pause")
        self.next_btn = ttk.Button(self.root_frame, text=">>")
        self.prev_btn = ttk.Button(self.root_frame, text="<<")
        
        self.next_btn.grid(column=1, row=2, sticky=(N, S, E))
        self.pause_btn.grid(column=1, row=2, sticky=(N, S, W))
        self.prev_btn.grid(column=1, row=2, sticky=(N, S, E))

    def show(self):
        self.root.mainloop()