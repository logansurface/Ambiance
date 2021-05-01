from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import serial

'''
A class for holding an array of color values, generated from the outer edges of an image
'''
class ColorFrame:
    border = False
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
        obj_str = f"\n<ColorFrame Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Capture Dimensions: {self.width} x {self.height}\n"
        obj_str += f"Border Shape: {self.border.shape}\n"
        obj_str += f"Color Channels: {self.screen.shape[2]}"

        return obj_str 

    '''
    Capture the screen and downscale it to avg. colors
    and reduce computational intensity
    '''
    def capture_frame(self, scale_factor = 4):
        # Capture the frame in screen_raw and set the width and height
        self.screen_raw = ImageGrab.grab()
        '''
        self.width, self.height = (self.screen_raw.width, self.screen_raw.height)
        self.width, self.height = (self.width // scale_factor, self.height // scale_factor)
        '''
        self.width, self.height = (self.hres, self.vres)

        # Convert the raw image to a rescaled version and create a numpy array from this
        self.screen = self.screen_raw.resize((self.width, self.height)).getdata()
        self.screen = np.array(self.screen, dtype=np.uint8).reshape(self.height, self.width, 3)

    '''
    Calculates the average color of the pixels within bounding boxes, specified by the
    screen dimensions and the resolution of the frame.
    '''
    def generate_border(self):
        # Initialize a numpy list with size col:vres x row:hres x depth:3
        # This list represents a BGR led array with a user specified resolution
        self.border = np.empty((self.vres, self.hres, 3), dtype=np.uint8)

        # Set the intervals and spacing as local vars to reduce the number of operations
        interval_x = self.width // self.hres
        interval_y = self.height // self.vres
        spacing_x = interval_x // 2
        spacing_y = interval_y // 2

        for y in range(self.vres):
            for x in range(self.hres):
                px = self.screen[(
                                int((y * interval_y) + spacing_y),
                                int((x * interval_x) + spacing_x)
                                )]
                self.border[y][x] = px
        
    '''
    Displays a graphical representation of the border using MatPlotLib
    '''
    def show_border(self):
        # Set the drawing area to be hres x vres
        plt.axis([0, self.hres - 1, 0, self.vres - 1])
        # Plot the top of the border
        plt.scatter(np.arange(self.hres),
                    np.zeros(self.hres)+(self.vres - 1),
                    c=self.border[0, : , : ]*(1/255), marker=',')
        # Plot the bottom of the border
        plt.scatter(np.arange(self.hres),
                    np.zeros(self.hres),
                    c=self.border[self.vres - 1, : , : ]*(1/255), marker=',')
        # Plot the left side of the border
        plt.scatter(np.zeros(self.vres),
                    np.arange(self.vres),
                    c=self.border[ : , 0, : ]*(1/255), marker=',')
        # Plot the right side of the border
        plt.scatter(np.zeros(self.vres)+(self.hres - 1),
                    np.arange(self.vres),
                    c=self.border[ : , self.hres - 1, : ]*(1/255), marker=',')
        plt.show()
        
    '''
    Returns a tuple representing the RGB value at the desired index
    @param x - The column value to retrieve the color from 
    @param y - The row value to retrieve the color from
    '''
    def get_border_color(self, x, y):
        if self.border is False:
            self.throw_not_processed()
        
        # The colors that were captured by OpenCV are stored as BGR
        # We want to convert this to an RGB colorspace
        bgr = self.border[y, x, : ]

        # Return the rotated color values
        return (bgr[2], bgr[1], bgr[0])
        
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
        print(self.screen_raw.mode)
        self.screen_raw.show()
    
    '''
    Throw this when the current frame has not been processed
    It will display an appropriate error message to the user
    and terminate program execution
    '''
    def throw_not_processed(self):
        print("Error, the current frame's border hasn't been generated yet.") 
        print("Generate the border using frame_obj.generate_border()")
        exit(-1)

# Run on program start
time = cv.getTickCount()

frame = ColorFrame(16, 8)
frame.capture_frame(4)
frame.generate_border()

delta_t = (cv.getTickCount() - time) / cv.getTickFrequency()

print(frame, "\n")
frame.show_border()

frame.print_border()
print("Processing Time: ", delta_t , "seconds")
print("Frame Rate: ", round(1 / delta_t), "frames per second")
print("Storage Type: ", frame.border.dtype)
print("-"*35 + "\n\n")