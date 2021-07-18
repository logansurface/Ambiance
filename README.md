# Ambiance
***
 **A python tool for creating ambient lighting via adressable led's based on the current screen state.**
***

## Hardware Needed
- A computer (Newer model Raspberry Pi's will probably suffice)
- A microcontroller capable of running Arduino code
- A Soldering Iron
- Stranded Hookup Wire
- Solder 
- Wire Strippers
- Around 3.5m of WS2811, WS2811b, or a WS2812 LED strips (based on a 50 inch television) 
- A 5v power source capable of delivering significant amounts of current. 3.5 meters of 60lpm strip, lit at full brightness, will draw an average of 10.2 Amperes.

## Code Dependencies
- The AmbianceController software ([Available on my GitHub](https://www.github.com/logansurface)), running on a suitable microcontroller, and connected to the host computer via USB.
- On the host computer the following dependencies will need to be installed via pip, an example is provided below.
- **Note:** pip does not come packaged with default Python installations and will need to be installed before proceeding.
***
    >> python -m pip install [package name]

    >> python -m pip install pillow
***
- Pillow (Image Capture)
- OpenCV-Python (Image Processing)
- Numpy (Fast N-Dimensional Arrays)
- MatPlotLib (Displaying Debugging Data)
- Serial (Sends color information to the microcontroller over USB)