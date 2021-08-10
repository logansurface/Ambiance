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
    app_name = "Ambiance v0.3"
    icon_path = "../res/icons/app_ico.png"
    framerate = 10 

    # Argument Parsing
    try:
        arg_list = sys.argv[1:]
        args, arg_values = getopt.getopt(arg_list, options, long_options)

        for current_arg, current_val in args:
            if current_arg in ("-h", "--help"):
                print("usage: python3 ambiance.py [-h] -x -y -p -b")
                print("\toptions:")
                print("\t\t-h, --help: show this help dialog")
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
        print(f"CLI Option Error: {str(err)}")
        exit(-1)

    #micro = Arduino(port, baud)
    time.sleep(2)

    '''
    Microcontroller Functionality Disabled

    if micro.is_connected():
        handshake = micro.receive()
        if handshake == 'R':
            print("Handshake established with microcontroller. Beginning data stream...")
            micro.send("R")
        else:
            print("Handshake cannot be established with microcontroller. Aborting...")
            exit(-1)
    else:
        print("Microcontroller not available on the specified port. Aborting...")
        exit(-1)
    '''

    '''
    GUI Disabled

    if(micro.is_connected()):
        main_window = MainWindow(app_name, icon_path, "CONNECTED", micro.port) 
    else:
        main_window = MainWindow(app_name, icon_path,"NOT CONNECTED", "PORT")

    main_window.show()
    '''

    cframe = ColorFrame(x_res, y_res)
    proc_ind = 1

    # Proc. loop, capture frames until interupt
    while True:
        print(f"\nFrame {proc_ind}")

        current_t = time.time()
        next_frame_t = current_t + (1.0 / framerate)
        tick = cv.getTickCount()

        cframe.capture_frame()
        flattened_border = cframe.generate_frame()
        led_ind = 1

        for pixel in flattened_border:
            '''
            Serial communication

            micro.send(f"{pixel[0]} ")    # Send R
            micro.send(f"{pixel[1]} ")    # Send G
            micro.send(f"{pixel[2]} ")    # Send B
            '''

            '''
            Color Debugging Output

            print(f"\tLED {led_ind}: [{pixel[0]}, ", end="")
            print(f"{pixel[1]}, ", end="")
            print(f"{pixel[2]}]")
            '''

            led_ind += 1

        led_ind = 0
        proc_ind += 1

        # Sleep until FPS target is met
        while(current_t < next_frame_t):
            current_t = time.time()
            if not current_t > next_frame_t:
                time.sleep(next_frame_t - current_t)

        # Display the framerate
        delta_t = (cv.getTickCount() - tick) / cv.getTickFrequency()
        print("Frame Rate: ", round(1 / delta_t), "frames per second")