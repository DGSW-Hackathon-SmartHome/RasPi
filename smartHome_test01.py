import serial
import time
import paho.mqtt.client as mqtt
import json
import re
import struct

#mqtt connect setting
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('smarthome/#')

#mqtt subscribe msg
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    try:
        j = json.loads(msg.payload)
        if msg.topic == 'smarthome/sensor/temperature':
            if j['type'] == 'aircon':
                if j['cmd'] == 'on':
                    arduino.write(b'A')
                else:
                    arduino.write(b'a')
            elif j['type'] == 'boiler':
                if j['cmd'] == 'on':
                    arduino.write(b'B')
                else:
                    arduino.write(b'b')
        elif msg.topic == 'smarthome/sensor/humidity':
            j = json.loads(msg.payload)
            if j['type'] == 'dehumidifier':
                if j['cmd'] == 'on':
                    arduino.write(b'D')
                else:
                    arduino.write(b'd')
            elif j['type'] == 'humidifier':
                if j['cmd'] == 'on':
                    arduino.write(b'H')
                else:
                    arduino.write(b'h')
        elif msg.topic == 'smarthome/sensor/air':
            j = json.loads(msg.payload)
            if j['type'] == 'fan':
                if j['cmd'] == 'on':
                    arduino.write(b'F')
                else:
                    arduino.write(b'f')
        elif msg.topic == 'smarthome/gasValve':
            j = json.loads(msg.payload)
            if j['type'] == 'gasvalve':
                if j['cmd'] == 'on':
                    arduino.write(b'G')
                else:
                    arduino.write(b'g')
        elif msg.topic == 'smarthome/sensor/led':
            j = json.loads(mas.payload)
            if j['type'] == 'livingroom':
                if j['cmd'] == 'on':
                    arduino.write(b'L')
                else:
                    arduino.write(b'l')
            elif j['type'] == 'room':
                if j['cmd'] == 'on':
                    arduino.write(b'R')
                else:
                    arduino.write(b'r')
            elif j['type'] == 'toilet':
                if j['cmd'] == 'on':
                    arduino.write(b'T')
                else:
                    arduino.write(b't')

    except Exception as e:
        print(e)
        pass

#mqtt client setting
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('3.34.177.215', 1883)
client.loop_start()

# 아두이노로부터 센서 값 받아오기
# ========================================================
# temperature       : T : 온도 값              : 
# aircon            : a : 에어컨 on/off        : 0, 1
# boiler            : b : 보일러 on/off        : 0, 1
# humidity          : H : 습도 값              : 
# humidifier        : h : 가습기 on/off        : 0, 1
# dehumidifier      : d : 제습기 on/off        : 0, 1
# air               : A : 미세먼지 값          : 
# fan               : f : 환풍기 on/off        : 0, 1
# gasvalve          : g : 가스밸브 on/off      : 0, 1
# livingroom led    : l : 거실 led on/off      : 0, 1
# room led          : r : 방 led on/off        : 0, 1
# toilet led        : t : 화장실 led on/off    : 0, 1
# ========================================================

regex = b'^T(.{2})a(.{1})b(.{1})H(.{2})h(.{1})d(.{1})A(.{4})f(.{1})g(.{1})l(.{1})r(.{1})t(.{1})\n$'
def read_arduino(ser)
    ser_msg = re.match(regex, ser.readline())
    if ser_msg is not None:
        temperature = int.from_bytes(ser_msg[1], byteorder='little')     # 온도 값갑
        aircon = int.from_bytes(ser_msg[2], byteorder='little')          # 에어컨 on/off
        boiler = (ser_msg[3]], byteorder='little')                       # 보일러 on/off
        humidity = int.from_bytes(ser_msg[4], byteorder='little')        # 습도 값
        humidifier = int.from_bytes(ser_msg[5], byteorder='little')      # 가습기 on/off
        dehumidifier = int.from_bytes(ser_msg[6], byteorder='little')    # 제습기 on/off
        air = struct.unpack('<f', ser_msg[7])[0]                         # 미세먼지 값
        fan = int.from_bytes(ser_msg[8], byteorder='little')             # 환풍기 on/off
        gasvalve = int.from_bytes(ser_msg[9], byteorder='little')        # 가스밸브 on/off
        livingroom = int.from_bytes(ser_msg[10], byteorder='little')     # 거실 led on/off
        room = int.from_bytes(ser_msg[11], byteorder='little')           # 방 led on/off
        toilet = int.from_bytes(ser_msg[12], byteorder='little')         # 화장실 led on/off

        return {
            'temperature': temperature,     # 온도 값
            'aircon': aircon,               # 에어컨 on/off
            'boiler': boiler,               # 보일러 on/off
            'humidity': humidity,           # 습도 값
            'humidifier': humidifier,       # 가습기 on/off
            'dehumidifier': dehumidifier,   # 제습기 on/off
            'air': air,                     # 미세먼지 값
            'fan': fan,                     # 환풍기 on/off
            'gasvalve': gasvalve            # 가스밸브 on/off
            'led':{                         # led on/off
                'livingroom': livingroom,   # 거실 led on/off
                'room': room,               # 방 led on/off
                'toilet': toilet            # 화장실 led on/off
            }
        }
    else:
        return None

try:
    global arduino
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

    arduino.flushInput()
    while True:
        data = read_arduino(arduino)
        if data is not None:
            print('{temperature}°C / {humidity}% / Air: {air:.2f}ppm'.format(**data))

            client.publish('smartfarm/value', json.dumps(data))

        client.loop_read()
        time.sleep(1)

    arduino.close()

except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)