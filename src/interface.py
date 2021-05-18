from tkinter import *
from tkinter import ttk

class MainWindow:
    def __init__(self, title: str):
        self._root = Tk()
        self._root.title(title)
        self.__add_menu()
        self.__add_frames()
        self.__add_canvas()
        self.__add_buttons()
        self.__add_labels()

    def __add_menu(self):
        self._menu_bar = Menu(self._root, tearoff=1)
        self._root.config(menu=self._menu_bar)

        self._file_menu = Menu(self._menu_bar)
        self._file_menu.add_command(label="Port")
        self._file_menu.add_command(label="Baudrate")
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Exit")

        self._help_menu = Menu(self._menu_bar)
        self._help_menu.add_command(label="How to use")
        self._help_menu.add_command(label="About")

        self._menu_bar.add_cascade(label="File", menu=self._file_menu)
        self._menu_bar.add_cascade(label="Help", menu=self._help_menu)

    def __add_frames(self, pad=3): 
        self._root_frame = ttk.Frame(self._root, padding=pad)
        self._root_frame.grid()
        self._ctrl_frame = ttk.Frame(self._root_frame)
        self._ctrl_frame.grid(column=1, row=2, columnspan=2)
        
    def __add_canvas(self, x=640, y=480):
        self._display = Canvas(self._root_frame, width=x, height=y, bg='gray12')
        self._display.grid(column=1, row=1 , sticky=(N, S, E, W))
        
        self._display.create_line(0, 0, 640, 480, dash=(3, 2), fill="#FFFF00")
        self._display.create_line(640, 0, 0, 480, dash=(3, 2), fill="#FFFF00")
    
    def __add_buttons(self):
        self._button_frame = ttk.Frame(self._ctrl_frame)
        self._button_frame.grid(column=1, row=0, sticky=(E))

        self._pause_btn = ttk.Button(self._button_frame, text="Pause")
        self._next_btn = ttk.Button(self._button_frame, text=">>")
        self._prev_btn = ttk.Button(self._button_frame, text="<<")
        
        self._next_btn.grid(column=2, row=0, rowspan=1)
        self._pause_btn.grid(column=1, row=0, rowspan=2, ipadx=15)
        self._prev_btn.grid(column=0, row=0, rowspan=1)
        
    def __add_labels(self, conn_status="NO CONNECTION", port=""):
        self._label_frame = ttk.Frame(self._ctrl_frame)
        self._label_frame.grid(column=0, row=0, sticky=(W))

        self._conn_label = ttk.Label(self._ctrl_frame, text=conn_status)
        self._port_label = ttk.Label(self._ctrl_frame, text=port)
        
        self._conn_label.grid(column=0)
        self._port_label.grid(column=1)

    def show(self):
        self._root.mainloop()