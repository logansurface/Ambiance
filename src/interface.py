from tkinter import *
from tkinter import ttk

import webbrowser

class MainWindow:
    default_font = ("dejavu sans mono", 11)
    menu_font = (default_font[0], default_font[1]-2)

    def __init__(self, title, icon_path, conn_status, port):
        self.root = Tk()
        self.root.title(title)
        self.style = ttk.Style()

        self.__set_icon(icon_path)
        self.__add_menus()
        self.__add_containing_frame(pad=10)
        self.__add_display(x=640, y=480, row=0)
        self.__add_buttons(row=1)
        self.__add_labels(conn_status, port, row=1)

    def __set_icon(self, icon_path):
        app_icon = PhotoImage(file=icon_path)
        self.root.iconphoto(False, app_icon)

    def __add_menus(self):
        root_menu = Menu(self.root)
        root_menu.configure(font=self.menu_font)
        self.root.config(menu=root_menu)

        self.port = StringVar()
        self.baud = StringVar()

        self.port_menu = Menu(root_menu, font=self.menu_font, tearoff=0)
        root_menu.add_cascade(label="Port", menu=self.port_menu)
        self.baud_menu = Menu(root_menu, font=self.menu_font, tearoff=0)
        root_menu.add_cascade(label="Baud", menu=self.baud_menu)
        self.help_menu = Menu(root_menu, font=self.menu_font, tearoff=0)
        root_menu.add_cascade(label="Help", menu=self.help_menu)

        self.port_menu.add_radiobutton(label="COM3", variable=self.port)
        self.port_menu.add_radiobutton(label="/dev/tty3", variable=self.port)

        self.baud_menu.add_radiobutton(label="9600", variable=self.baud, command=lambda: print(self.baud.get()))
        self.baud_menu.add_radiobutton(label="19200", variable=self.baud, command=lambda: print(self.baud.get()))
        self.baud_menu.add_radiobutton(label="38400", variable=self.baud, command=lambda: print(self.baud.get()))
        self.baud_menu.add_radiobutton(label="57600", variable=self.baud, command=lambda: print(self.baud.get()))
        self.baud_menu.add_radiobutton(label="115200", variable=self.baud, command=lambda: print(self.baud.get()))

        self.help_menu.add_command(label="How to Use", command=lambda: webbrowser.open("www.github.com/logansurface/Ambiance", new=0, autoraise=True))
        self.help_menu.add_command(label="Report a Bug", command=lambda: webbrowser.open("www.github.com/logansurface/Ambiance/issues", new=0, autoraise=True))
        self.help_menu.add_command(label="View Source", command=lambda: webbrowser.open("www.github.com/logansurface/Ambiance/tree/main/src", new=0, autoraise=True))
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About")

    def __add_containing_frame(self, pad): 
        self.root_frame = ttk.Frame(self.root, padding=pad)
        self.root_frame.grid()
        self.root_frame.columnconfigure(0, weight=2)
        self.root_frame.columnconfigure(1, weight=5)
        self.root_frame.columnconfigure(2, weight=1)
        self.root_frame.columnconfigure(3, weight=1)
        self.root_frame.columnconfigure(4, weight=1)
        
    def __add_display(self, x, y, row):
        dframe = PhotoImage()

        self.display = Canvas(self.root_frame, width=x, height=y, background='gray12')
        self.display.grid(column=0, row=row, columnspan=self.root_frame.grid_size()[0], pady=(0, 10))

    def __add_labels(self, conn_status, port, row):
        self.style.configure("port.TLabel", font=self.default_font, foreground="#00BD86")
        self.port_label = ttk.Label(self.root_frame, text=port+" - "+conn_status, style="port.TLabel")
        self.spacer = ttk.Label(self.root_frame, text='')

        self.port_label.grid(column=0, row=row, sticky='w')
        self.spacer.grid(column=1, row=row, sticky='w')
    
    def __add_buttons(self, row):
        self.style.configure("TButton", font=self.default_font, relief="none")
        self.prev_btn = ttk.Button(self.root_frame, text=u"\u25C0")
        self.pause_btn = ttk.Button(self.root_frame, text=u"\u25A0")
        self.next_btn = ttk.Button(self.root_frame, text=u"\u25B6")

        self.prev_btn.grid(column=2, row=row, sticky=(E))
        self.pause_btn.grid(column=3, row=row, sticky=(E))
        self.next_btn.grid(column=4, row=row, sticky=(E))

    def show(self):
        self.root.mainloop()