import serial
port = 'COM4'
baud = 9600

ser = serial.Serial()
ser.port = port
ser.baudrate = baud
ser.open()

def doConvDiv():
    ser.write(65)
    line = ser.readline()
    return int(line)
