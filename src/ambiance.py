from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np

import serial

# A class for holding an array of color values, 
# generated from the outer edges of an image
class ColorFrame:
    border = None
    height = 0
    width = 0

    # @param hres - the number of horizontal points needed
    # @param vres - the number of vertical points needed
    def __init__(self, hres, vres):
        self.hres = hres
        self.vres = vres
    
    def __str__(self):
        return f"CDimensions: {self.width} x {self.height}\nColor Channels: {self.screen.shape[2]}"
    
    # Capture the screen and downscale it to avg. colors
    # and reduce computational intensity
    def capture_frame(self, scale_factor = 4):
        # Capture the frame in screen_raw and set the width and height
        self.screen_raw = ImageGrab.grab()
        self.width, self.height = self.screen_raw.size
        self.width, self.height = self.width // scale_factor, self.height // scale_factor

        # Convert the raw image to a rescaled version and create a numpy array from this
        self.screen = self.screen_raw.resize((self.width, self.height)).getdata()
        self.screen = np.array(self.screen, dtype=np.uint8).reshape(self.height, self.width, 3)

    # Calculates the average color of the pixels within bounding boxes, specified by the
    # screen dimensions and the resolution of the frame.
    def generate_border(self):
        self.border = np.empty((self.height, self.width, 3), dtype=np.uint8)
        # Set the intervals and spacing as local variables to reduce number of operations
        interval_x = self.width // self.hres
        interval_y = self.height // self.vres
        spacing_x = interval_x // 2
        spacing_y = interval_y // 2

        for y in range(self.vres):
            for x in range(self.hres):
                px = self.screen[(int(y * interval_y) + spacing_y), int((x * interval_x) + spacing_x)]  
                self.border[y][x] = px
                print(f"[{y}][{x}]: {px}")

    # SHow the processed frame
    def show_frame(self):
        #disp = cv.cvtColor(self.screen, cv.COLOR_BGR2GRAY)
        cv.imshow("Show Frame", self.screen)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Show the original frame that was captured
    def show_original_frame(self):
        self.screen_raw.show()

# Run on program start
time = cv.getTickCount()
frame = ColorFrame(16, 8)
frame.capture_frame(4)
frame.generate_border()
print(frame.border.ndim)

print((cv.getTickCount() - time) / cv.getTickFrequency())
print(frame)
#frame.show_frame()