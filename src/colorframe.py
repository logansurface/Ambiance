from PIL import Image, ImageGrab

import numpy as np
import matplotlib.pyplot as plt

class ColorFrame:
    '''
    An object holding NxM RGB values, generated from the outer edges of an image.
    Where N is a specified sample resolution for the width of the image and M is the
    sample resolution for the height of an image.
    '''

    frame_generated = False

    def __init__(self, hres, vres):
        '''
        @param hres : int - the number of horizontal points needed
        @param vres : int - the number of vertical points needed
        '''
        self.hres = hres
        self.vres = vres
    
    def __str__(self):
        obj_str = f"\n<ColorFrame Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Capture Dimensions: {self.screen_raw.width} x {self.screen_raw.height}\n"
        obj_str += f"Color Channels: {self.screen.shape[2]}\n"

        # Append the border to string, if it's been generated
        if not self.frame_generated is False:
            obj_str += f"Frame Shape: {self.hres}x{self.vres}\n"

        return obj_str

    def capture_frame(self):
        '''
        Capture the screen and downscale it to avg. colors
        and reduce computational intensity
        '''
        self.screen_raw = ImageGrab.grab()
        self.screen = self.screen_raw.resize((self.hres, self.vres), Image.NEAREST)

    def generate_frame(self):
        ''' 
        Grab the edge pixels from the downsampled image
        @returns a flattened numpy.ndarray containing the frame in the order L, T, R, B
        '''
        self.left = np.empty((self.vres, 3), dtype=np.uint8)
        self.right = np.empty((self.vres, 3), dtype=np.uint8)
        self.top = np.empty((self.hres, 3), dtype=np.uint8)
        self.bottom = np.empty((self.hres, 3), dtype=np.uint8)

        for y in range(self.vres):
            self.left[y] = self.screen.getpixel((0, self.vres-y-1))
            self.right[y] = self.screen.getpixel((self.vres-1, self.vres-y-1))

        for x in range(self.hres):
            self.top[x] = self.screen.getpixel((x, 0))
            self.bottom[x] = self.screen.getpixel((x, self.vres-1))

        self.frame_generated = True
        return np.concatenate((self.left, self.top, self.right, self.bottom))
 
    def plot_frame(self):
        '''
        Display a graphical representation of the frame using MatPlotLib
        '''
        if self.frame_generated is False:
            self.throw_not_processed()

        # Set the drawing area to be hres x vres
        plt.axis([-1, self.hres, -1, self.vres])
        plt.suptitle("screen")

        # Plot the right side of the frame 
        plt.scatter(np.zeros(self.vres-2)+(self.hres - 1),
                    np.arange(self.vres-2)+1,
                    c=self.right[1:self.vres-1, : ]*(1/255),
                    marker=',')
        # Plot the left side of the frame
        plt.scatter(np.zeros(self.vres-2),
                    np.arange(self.vres-2)+1,
                    c=self.left[1:self.vres-1, : ]*(1/255),
                    marker=',')
        # Plot the top of the frame
        plt.scatter(np.arange(self.hres),
                    np.zeros(self.hres)+(self.vres - 1),
                    c=self.top[...]*(1/255),
                    marker=',')
        # Plot the bottom of the frame 
        plt.scatter(np.arange(self.hres),
                    np.zeros(self.hres),
                    c=self.bottom[...]*(1/255),
                    marker=',')
        plt.show()

    def show_capture(self):
        '''
        Show the original capture, before processing was applied
        '''
        self.screen_raw.show()
    
    def throw_not_processed(self):
        '''
        Throw when the current frame has not been processed
        '''
        print("Error, the current frame hasn't been generated yet.") 
        print("Generate the border using frame_obj.generate_frame()\n")
        exit(-1)