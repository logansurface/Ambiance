import serial

class Arduino:
    '''
    Object type representing an Arduino based microcontroller,
    using serial communication on the specified port.
    '''
    _is_connected = True

    def __init__(self, port, baud):
        '''
        @param port: string - The serial port the arduino is connected to (/dev/tty# or COM<#>)
        @param baud: int - The baud rate of the device's serial port (communication speed)
        '''
        self.port = port
        self.baud = baud

        try:
            self._txrx = serial.Serial(port=port, baudrate=baud)
        except serial.SerialException:
            self._is_connected = False
        
    def __str__(self):
        obj_str = f"\n<Arduino Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Port: {self.port}\n"
        obj_str += f"Baud Rate: {self.baud}\n"

        return obj_str

    def is_connected(self):
        '''
        Check the serial object to see if it has been opened properly
        @return bool: True if serial is open, False if serial is closed
        '''
        return self._is_connected

    def send(self, data: str):
        '''
        Write to the serial port's output stream
        @param data: string - data to write
        ''' 
        try:
            self._txrx.write(data.encode("utf-8"))
        except AttributeError as err:
            print(f"{data} is the wrong type. Try sending a string.")
            exit(-1)

    def recieve(self):
        '''
        Read from the serial port's output stream
        @return a decoded utf-8 string
        '''
        return self._txrx.read().decode("utf-8")
