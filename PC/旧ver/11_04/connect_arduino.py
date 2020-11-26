import serial
import time

# ポートの指定
def initialize(port, bps):
    port = serial.Serial(port, bps)
    time.sleep(2)
    return port


# arduinoへのデータ送信
def send_command(port, byte):
    port.write(byte)
    data = wait_response(port)
    return data

# arduinoから返信されるシリアル内容の表示
def wait_response(port):
    while 1:
        if port.in_waiting > 0:
            time.sleep(0.01)
            data = port.read_all().decode('utf-8')
            print(data)
            break
    return data

def light_switch():
    led = {'ON': b"a", 'OFF': b"b", 'Orange':b"c"}
    tv = {'Power': b"d", 'UP': b"e", 'Down': b"f"}
    ir_read = {'read': b"r"}

    port1 = initialize("COM7", 9600)
    send_command(port1, led['ON'])
    port1.close()
    print('照明を付けます')

def pressure_reset():
    pressure = {'reset':b"g", 'init': b"s", 'get':b"w"}
    port2 = initialize("COM10", 115200)
    send_command(port2, pressure['reset'])
    port2.close()

def pressure_init():
    pressure = {'reset':b"g", 'init': b"s", 'get':b"w"}
    port2 = initialize("COM10", 115200)
    send_command(port2, pressure['init'])
    port2.close()

def pressure_get():
    pressure = {'reset':b"g", 'init': b"s", 'get':b"w"}
    port2 = initialize("COM10", 115200)
    press_data = send_command(port2, pressure['get'])
    port2.close()
    return press_data

def Servomotor():
    port3 = initialize('COM9', 9600)
    send_command(port3, b'm')
    port3.close()
