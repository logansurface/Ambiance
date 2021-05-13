import serial

class Arduino:
    '''
    @param port : string - The serial port the arduino is connected to (/dev/tty# or COM<#>)
    @param baud : int - The baud rate of the device's serial port (communication speed)
    '''
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.txrx = serial.Serial(port=port, baudrate=baud)

    def __str__(self):
        obj_str = f"\n<Arduino Object @ {hex(id(self))}>\n"
        obj_str += "-"*35 + "\n"
        obj_str += f"Port: {self.port}\n"
        obj_str += f"Baud Rate: {self.baud}\n"

        return obj_str

    '''
    Write to the serial port's output stream
    @param data : string - data to write
    ''' 
    def send(self, data):
        self.txrx.write(data.encode("utf-8"))

    '''
    Read from the serial port's output stream
    '''
    def read(self):
        return self.txrx.read().decode("utf-8")