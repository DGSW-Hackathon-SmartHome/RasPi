import serial
import time
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('smarthome/#')

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        j = json.loads(msg.payload)
        if msg.topic == 'smarthome/sensor/temperature':
            if j['type'] == 'aircon':
                if j['cmd'] == 'on':
                    print("aricon on")
                    #arduino.write(b'A')
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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('3.34.177.215', 1883)
client.loop_start()

try:
    print("실행")
    while True:
        client.loop_read()
        time.sleep(1)    

except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)