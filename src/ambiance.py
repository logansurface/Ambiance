from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np

import serial

'''
A class for holding an array of color values, 
generated from the outer edges of an image
'''
class ColorFrame:
    border = None
    height = 0
    width = 0

    '''
    Constructor for the ColorFrame
    @param hres - the number of horizontal points needed
    @param vres - the number of vertical points needed
    '''
    def __init__(self, hres, vres):
        self.hres = hres
        self.vres = vres
    
    def __str__(self):
        return f"Capture Dimensions: {self.width} x {self.height}\nBorder Dimensions: {self.border.shape}\nColor Channels: {self.screen.shape[2]}"
    
    '''
    Capture the screen and downscale it to avg. colors
    and reduce computational intensity
    '''
    def capture_frame(self, scale_factor = 4):
        # Capture the frame in screen_raw and set the width and height
        self.screen_raw = ImageGrab.grab()
        self.width, self.height = self.screen_raw.size
        self.width, self.height = self.width // scale_factor, self.height // scale_factor

        # Convert the raw image to a rescaled version and create a numpy array from this
        self.screen = self.screen_raw.resize((self.width, self.height)).getdata()
        self.screen = np.array(self.screen, dtype=np.uint8).reshape(self.height, self.width, 3)

    '''
    Calculates the average color of the pixels within bounding boxes, specified by the
    screen dimensions and the resolution of the frame.
    '''
    def generate_border(self):
        # Initialize a numpy list with size col:vres x row:hres x depth:3
        # This list represents a BGR led array with user specified resolution
        self.border = np.empty((self.vres, self.hres, 3), dtype=np.uint8)

        # Set the intervals and spacing as local vars to reduce the number of operations
        interval_x = self.width // self.hres
        interval_y = self.height // self.vres
        spacing_x = interval_x // 2
        spacing_y = interval_y // 2

        for y in range(self.vres):
            for x in range(self.hres):
                px = self.screen[(int(y * interval_y) + spacing_y), int((x * interval_x) + spacing_x)]  
                self.border[y][x] = px
        
    '''
    Print out the ColorFrame in a human readable form 
    '''
    def print_frame(self):
        try:
            print("Top Row:\n", self.border[0, ...], '\n')
            print("Bot Bow:\n", self.border[self.vres - 1, ...], '\n')
            print("Left Col:\n", self.border[1:self.vres - 1, 0, : ], '\n')
            print("Right Col:\n", self.border[1:self.vres - 1, self.hres - 1, : ])
        except TypeError:
            print("Error, the current frame hasn't been generated yet.") 
            print("Generate the frame using frame_obj.generate_border()")
            exit(-1)

    '''
    Show the processed capture
    '''
    def show_processed_capture(self):
        disp = cv.cvtColor(self.screen, cv.COLOR_BGR2GRAY)
        cv.imshow("Show Frame", disp)
        cv.waitKey(0)
        cv.destroyAllWindows()

    '''
    Show the original capture, before processing was applied
    '''
    def show_capture(self):
        self.screen_raw.show()

# Run on program start
time = cv.getTickCount()

frame = ColorFrame(16, 8)
frame.capture_frame()
frame.generate_border()
delta_t = (cv.getTickCount() - time) / cv.getTickFrequency()
frame.print_frame()

print("Processing Time: ", delta_t , "Sec.")
print("Frame Rate: ", (1 / delta_t), "FPS")
print(frame, "\n")
frame.show_capture()