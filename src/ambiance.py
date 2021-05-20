import cv2 as cv

from interface import MainWindow
from colorframe import ColorFrame
from arduino import Arduino

if __name__ == "__main__":
    app_name = "Ambiance v0.1"
    micro = Arduino('/dev/tty3', 115200)

    if(micro.is_connected):
        main_window = MainWindow(app_name, "CONNECTED", micro.port) 
    else:
        main_window = MainWindow(app_name, "NOT CONNECTED", "PORT")

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