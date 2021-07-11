# Ambiance
***
 **A python tool for creating ambient lighting via adressable led's based on the current screen state.**

## Hardware Needed
- A computer (Newer model Raspberry Pi's will probably suffice)
- A microcontroller capable of running Arduino code
- A Soldering Iron
- Stranded Hookup Wire
- Solder 
- Wire Strippers
- Around 3.4m of WS2811, WS2811b, or a WS2812 LED strips (based on a 50 inch television) 
- A 5v power source capable of delivering significant amounts of current. At 60 led's per meter, with 3.4 meters of strip, when lit at full brightness the leds will draw an average of 10.2 Amperes.

## Code Dependencies
- These will need to be installed via pip, an example is provided below.
- **Note:** pip does not come packaged with python installations and will need to be installed before proceeding.
***
    python -m pip install [package name]

    python -m pip install pillow
***
- Pillow (Image Capture)
- OpenCV-Python (Image Processing)
- Numpy (Fast N-Dimensional Arrays)
- MatPlotLib (Displaying Debugging Data)
- Serial (Sends color information to the microcontroller over USB)