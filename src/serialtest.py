import serial

if __name__ == "__main__":
    micro = serial.Serial("COM7", baudrate=115200)

    try:
        while True:
            data = "["
            data = data + input("Command: ") + "]"
            micro.write(data.encode("utf-8"))
            print("COM7 -> ", micro.read().decode("utf-8"))
    finally:
        micro.close()
