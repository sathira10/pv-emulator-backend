from serial import Serial, serialutil
import struct
from time import sleep

READ_TIME = 0.2
BAUDRATE = 115200


def new_connection(port):
    try:
        ser = Serial(port=port, baudrate=BAUDRATE)
        return ser, "connected"
    except serialutil.SerialException:
        return None, "not connected"


def close_connection(ser: Serial):
    try:
        ser.close()
        return "connection closed"
    except AttributeError:
        return "no connection to close"


def update_parameters(ser: Serial, iph: float, io: float, rs: float, rsh: float, a: float, isc: float):
    x = struct.pack('?6f', True, iph, io * 1e10, rs, rsh, a, isc)
    ser.reset_output_buffer()
    ser.write(x)
    print("parameters updated")
    sleep(READ_TIME)
    ser.reset_input_buffer()


def read(ser: Serial):
    x = struct.pack('?6f', False, 0, 0, 0, 0, 0, 0)

    ser.reset_output_buffer()
    ser.reset_input_buffer()

    ser.write(x)
    sleep(READ_TIME)
    try:
        line = ser.readline()[:-1]
        return struct.unpack('3f', line)
    except Exception as e:
        print(str(e))
