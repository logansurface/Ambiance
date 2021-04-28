from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np
import serial

class ColorFrame:
    screen = None
    height = 0
    width = 0

    def __init__(self, vres, hres):
        self.vres = vres
        self.hres = hres
    
    def __str__(self):
        return f"{self.width} x {self.height}"
    
    # Capture the screen and downscale it to avg. colors
    # and reduce computational intensity
    def capture_frame(self, scale_factor = 4):
        self.screen = ImageGrab.grab()
        self.width, self.height = self.screen.size
        self.width, self.height = self.width // scale_factor, self.height // scale_factor
        self.screen = self.screen.resize((self.width, self.height))

    def show_frame(self):
        self.screen.show()

    # TODO - Grab ave. colors from the outer frame of the screen
    def extract_borders(self):
        pass

time = cv.getTickCount()
frame = ColorFrame(8, 16)
frame.capture_frame(4)

print((cv.getTickCount() - time) / cv.getTickFrequency())
print(f"frame: {frame}")

frame.show_frame()

#screen_np = np.array(capture_frame())

#cframe = cv.cvtColor(screen_np, cv.COLOR_BGR2GRAY)
#cv.imshow("Ambiance", cframe)
#cv.waitKey(0)
#cv.destroyAllWindows()