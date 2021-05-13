import cv2 as cv

from interface import MainWindow
from colorframe import *
from arduino import *

if __name__ == "__main__":
    main_window = MainWindow("Ambiance v0.1") 
    micro = Arduino('COM3', 115200)

    frame = ColorFrame(32, 18)   # Frame generated for 30 lpm strip
    #frame = ColorFrame(64, 36)  # Frame generated for 60 lpm strip
    #frame = ColorFrame(158, 86) # Frame generated for 144 lpm strip
    
    main_window.show()

    '''
    # Proc. loop, capture frames until interupt
    while True:
        tick = cv.getTickCount()     # Tick ref. for calculating runtime
        frame.capture_frame()

        frame.generate_frame()
        #data = frame.generate_frame()
        #micro.send(packet)

        delta_t = (cv.getTickCount() - tick) / cv.getTickFrequency()
        print("Frame Rate: ", round(1 / delta_t), "frames per second")
    '''