import cv2 as cv
import time

from interface import MainWindow
from colorframe import ColorFrame
from arduino import Arduino

if __name__ == "__main__":
    app_name = "Ambiance v0.2"
    icon_path = "../res/icons/app_ico.png"

    cframe = ColorFrame(32, 18)
    micro = Arduino('/dev/tty3', 115200)
    time.sleep(2)

    '''
    if(micro.is_connected()):
        main_window = MainWindow(app_name, icon_path, "CONNECTED", micro.port) 
    else:
        main_window = MainWindow(app_name, icon_path,"NOT CONNECTED", "PORT")

    main_window.show()
    '''

    '''
    Attempt to establish a handshake with the MCU,
    so that preliminary information can be sent
    '''
    if micro.is_connected():
        handshake = micro.recieve()
        if handshake == 'R':
            print("Handshake established with microcontroller. Beginning data stream...")
            micro.send((cframe.hres*2) + (cframe.vres*2))   # Send the bits per frame
        else:
            print("Handshake can not be established with microcontroller. Aborting...")
            exit(-1)
    else:
        print("Error: Microcontroller not available on the specified port. Aborting...")
        exit(-1)

    # Proc. loop, capture frames until interupt
    while True:
        tick = cv.getTickCount()

        cframe.capture_frame()
        flattened_border = cframe.generate_frame()

        for pixel in flattened_border:
            micro.send(pixel[0])    # Send R
            micro.send(pixel[1])    # Send G
            micro.send(pixel[2])    # Send B

        delta_t = (cv.getTickCount() - tick) / cv.getTickFrequency()
        print("Frame Rate: ", round(1 / delta_t), "frames per second")