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
    print(msg.topic, msg.payload)
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
regex = b'^T(.{2})H(.{2})A(.{4})G(.{3})\n$'
def read_arduino(ser)
    ser_msg = re.match(regex, ser.readline())
    if ser_msg is not None:
        temperature = int.from_bytes(ser_msg[1], byteorder='little')
        humidity = int.from_bytes(ser_msg[2], byteorder='little')
        air = struct.unpack('<f', m[3])[0]
        gasvalve = ser_msg[4].decode('utf-8')

        return {
            'humidity': humidity,
            'temperature': temperature,
            'air': air,
            'gasvalve': gasvalve
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
            print('{humidity}% / {temperature}°C / Air: {air:.2f}ppm / gasValve: {gasValve}'.format(**data))

            client.publish('smartfarm/value', json.dumps(data))

        client.loop_read()
        time.sleep(1)    

    arduino.close()

except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)