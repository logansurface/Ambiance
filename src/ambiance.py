from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import serial
import time as systime

'''
A class for holding an array of color values, generated from the outer edges of an image
'''
class ColorFrame:
    border = False

    '''
    Constructor for the ColorFrame
    @param hres - the number of horizontal points needed
    @param vres - the number of vertical points needed
    '''
    def __init__(self, hres, vres):
        self.hres = hres
        self.vres = vres
    
    def __str__(self):
        obj_str = f"\n<ColorFrame Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Capture Dimensions: {self.screen_raw.width} x {self.screen_raw.height}\n"
        obj_str += f"Color Channels: {self.screen.shape[2]}\n"

        # Append the border to string, if it's been generated
        if not self.border is False:
            obj_str += f"Border Shape: {self.border.shape}\n"

        return obj_str 

    '''
    Capture the screen and downscale it to avg. colors
    and reduce computational intensity
    '''
    def capture_frame(self):
        # Capture the frame in screen_raw
        self.screen_raw = ImageGrab.grab()

        # Convert the raw image to a rescaled version and create a numpy array from this
        self.screen = self.screen_raw.resize((self.hres, self.vres)).getdata()
        self.screen = np.array(self.screen, dtype=np.uint8).reshape(self.vres, self.hres, 3)

    '''
    Calculates the average color of the pixels within bounding boxes, specified by the
    screen dimensions and the resolution of the frame.
    '''
    def generate_border(self):
        # Initialize a numpy list with size col:vres x row:hres x depth:3
        # This list represents an RGB led array with a user specified resolution
        self.border = np.empty((self.vres, self.hres, 3), dtype=np.uint8)

        for y in range(self.vres):
            for x in range(self.hres):
                self.border[y][x] = self.screen[(y, x)] 

        return self.border
        
    '''
    Displays a graphical representation of the border using MatPlotLib
    '''
    def show_border(self):
        if self.border is False:
            self.throw_not_processed()

        # Set the drawing area to be hres x vres
        plt.axis([-1, self.hres, -1, self.vres])
        plt.suptitle("Screen")

        # Plot the top of the border
        plt.scatter(np.arange(self.hres),
                    np.zeros(self.hres)+(self.vres - 1),
                    c=self.border[0, : , : ]*(1/255),
                    marker=',')
        # Plot the bottom of the border
        plt.scatter(np.arange(self.hres),
                    np.zeros(self.hres),
                    c=self.border[self.vres - 1, : , : ]*(1/255),
                    marker=',')
        # Plot the left side of the border
        plt.scatter(np.zeros(self.vres),
                    np.arange(self.vres),
                    c=self.border[ : , 0, : ]*(1/255),
                    marker=',')
        # Plot the right side of the border
        plt.scatter(np.zeros(self.vres)+(self.hres - 1),
                    np.arange(self.vres),
                    c=self.border[ : , self.hres - 1, : ]*(1/255),
                    marker=',')

        plt.show()

    '''
    Return the border, resized in the x and y by a factor provided.
    This is helpful for displaying the frame's colors in OpenCV's imshow()

    Example:
    border.shape = (32, 18, 3) -> scale_border(2) -> border.shape = (64, 36, 3)
    '''
    def scale_border(self, factor):
        border_sc = np.zeros((self.vres*factor, self.hres*factor, self.screen.shape[2]), dtype=np.uint)

        i, j = (0, 0)
        for y in np.arange(0, self.vres - 2, factor):
            for x in np.arange(0, self.hres - 2, factor):
                border_sc[y:y+factor, x:x+factor,...] = self.border[i][j]
                j = j + 1
            i = i + 1 

        return border_sc
        
    '''
    Print out the ColorFrame in a human readable form 
    '''
    def print_border(self):
        if self.border is False:
            self.throw_not_processed()

        print("Top:\n", self.border[0, ...], '\n')
        print("Left:\n", self.border[1:self.vres - 1, 0, : ], '\n')
        print("Right:\n", self.border[1:self.vres - 1, self.hres - 1, : ], '\n')
        print("Bottom:\n", self.border[self.vres - 1, ...], '\n')

    '''
    Show the original capture, before processing was applied
    '''
    def show_capture(self):
        self.screen_raw.show()
    
    '''
    Throw this when the current frame has not been processed
    It will display an appropriate error message to the user
    and terminate program execution
    '''
    def throw_not_processed(self):
        print("Error, the current frame's border hasn't been generated yet.") 
        print("Generate the border using frame_obj.generate_border()\n")
        exit(-1)

class Arduino:
    '''
    Constructor for the Arduino object
    @param port - The serial port the arduino is connected to (/dev/tty# or COM<#>)
    @param baud - The baud rate of the device's serial port (communication speed)
    '''
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.txrx = serial.Serial(port=port, baudrate=baud, timeout=0.1)

    def __str__(self):
        obj_str = f"\n<Arduino Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Port: {self.port}\n"
        obj_str += f"Baud Rate: {self.baud}\n"

        return obj_str
    
    def send(self, data):
        self.txrx.write(packet)
        time.sleep(0.1)

if __name__ == "__main__":
    micro = Arduino('COM3', 115200)

    frame = ColorFrame(32, 18)   # Frame generated for 30 lpm strip
    #frame = ColorFrame(64, 36)  # Frame generated for 60 lpm strip
    #frame = ColorFrame(158, 86) # Frame generated for 144 lpm strip


    # Proc. loop, capture frames until interupt
    while True:
        tick = cv.getTickCount()     # Tick ref. for calculating runtime
        frame.capture_frame()

        packet = frame.generate_border().flatten()
        micro.send(packet)

        #cv.imshow("capture", frame.scale_border(5))

        delta_t = (cv.getTickCount() - tick) / cv.getTickFrequency()

        print("Frame Rate: ", round(1 / delta_t), "frames per second")