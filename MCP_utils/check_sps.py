import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 230400, timeout=None) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.

ser.reset_output_buffer()
ser.reset_input_buffer()

while True:
    start = time.time()
    a = b'\x50'
    ## start using ser.write(<data-in-bytes>)
    data = ser.read(500)
    end = time.time()
    print(end - start)
