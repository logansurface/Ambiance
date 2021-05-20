import serial

class Arduino:
    '''
    @param port: string - The serial port the arduino is connected to (/dev/tty# or COM<#>)
    @param baud: int - The baud rate of the device's serial port (communication speed)
    '''
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud

        try:
            self._txrx = serial.Serial(port=port, baudrate=baud)
        except serial.SerialException as s:
            print(s)

    def __str__(self):
        obj_str = f"\n<Arduino Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Port: {self.port}\n"
        obj_str += f"Baud Rate: {self.baud}\n"

        return obj_str

    '''
    Check the serial object to see if it has been closed
    @return bool: true if serial is open, false if serial is closed
    '''
    def is_connected(self):
        return self._txrx.closed

    '''
    Write to the serial port's output stream
    @param data: string - data to write
    ''' 
    def send(self, data):
        self._txrx.write(data.encode("utf-8"))

    '''
    Read from the serial port's output stream
    @return a decoded utf-8 string
    '''
    def recieve(self):
        return self._txrx.read().decode("utf-8")
