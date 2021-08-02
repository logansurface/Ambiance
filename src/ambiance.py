import time
import getopt, sys

import cv2 as cv

from interface import MainWindow
from colorframe import ColorFrame
from arduino import Arduino

options = "hx:y:p:b:"
long_options = [
    "help",
    "x_res =",
    "y_res =",
    "port =",
    "baud ="
]

if __name__ == "__main__":
    app_name = "Ambiance v0.2"
    icon_path = "../res/icons/app_ico.png"

    # Argument Parsing
    try:
        arg_list = sys.argv[1:]
        args, arg_values = getopt.getopt(arg_list, options, long_options)

        for current_arg, current_val in args:
            if current_arg in ("-h", "--help"):
                print("usage: python3 ambiance.py [-h] -x -y -p -b")
                print("\toptions")    
                print("\t\t-h, --help: show this dialog.")
                print("\t\t-x, --x_res: number of leds across horizontal axis")
                print("\t\t-y, --y_res: number of leds across vertical axis")
                print("\t\t-p, --port: local dev. name of serial port [ex: COM3]")
                print("\t\t-b, --baud: serial communication speed of device [typically 115200]\n")
                exit(0)
            elif current_arg in ("-x", "--x_res"):
                x_res = int(current_val)
            elif current_arg in ("-y", "--y_res"):
                y_res = int(current_val)
            elif current_arg in ("-p", "--port"):
                port = current_val
            elif current_arg in ("-b", "--baud"):
                baud = int(current_val)
    except getopt.error as err:
        print(str(err))
        exit(-1)

    micro = Arduino(port, baud)
    time.sleep(2)
    micro.handshake('R')

    '''
    GUI Disabled (under development)

    if(micro.is_connected()):
        main_window = MainWindow(app_name, icon_path, "CONNECTED", micro.port) 
    else:
        main_window = MainWindow(app_name, icon_path,"NOT CONNECTED", "PORT")

    main_window.show()
    '''

    cframe = ColorFrame(x_res, y_res)

    # Proc. loop, capture frames until interupt
    while True:
        tick = cv.getTickCount()

        # Ensure a valid connection exists
        if micro.receive() == 'R':
            micro.handshake('R')

        # Capture frame and generate border pixels
        cframe.capture_frame()
        flattened_border = cframe.generate_frame()

        for pixel in flattened_border:
            micro.send(f"{pixel[0]} ")    # Send R
            micro.send(f"{pixel[1]} ")    # Send G
            micro.send(f"{pixel[2]} ")    # Send B

        delta_t = (cv.getTickCount() - tick) / cv.getTickFrequency()
        print("Frame Rate: ", round(1 / delta_t), "frames per second")