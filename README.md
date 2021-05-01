# Ambiance
 A python tool for creating ambient lighting via adressable led's based on the current screen state.

## Hardware Needed
- A computer
- A microcontroller capable of running Arduino code (I used an ESP-32, a Teensy-LC would work fine too)
- A Soldering Iron
- Stranded Hookup Wire, 26-28 AWG is fine for our purposes
- Solder (Using leaded over lead free will make it significantly easier to create reliable connections)
- Wire Strippers, if your're not a masochist like myself
- Around 5m of WS2811, WS2811b, or a WS2812 LED strips (based on a 50 inch television) 
- A 5v power source, capable of delivering 1.5-2.0 Amps

## Code Dependencies
- Pillow (Image Capture)
- OpenCV-Python (Image Processing)
- Numpy (Fast N-Dimensional Arrays)
- MatPlotLib (Displaying Data)
- Serial (Sends color information to the microcontroller over USB)