#MQTT TestmqttClient GUI
import paho.mqtt.client as mqtt
from time import sleep
import threading
import time
import sys
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import (IMU, Camera, Damage, Electrics, Lidar, State, Timer, Ultrasonic)
from beamngpy.sensors import AdvancedIMU
import json

# open BeamNG at it's location
print (">>> open BeamNG")

beamng = BeamNGpy('127.0.0.1', 64256, home='C:\BeamNG\BeamNG.tech.v0.28.1.0')
beamng.open()

print (">>> create scenario in BeamNG")
# create a scenario with the map 'gridmap' and name the scenario 'Car IT'
scenario = Scenario('italy', 'Car IT')
#scenario = Scenario('smallgrid', 'Car IT')


print (">>> create vehicle in BeamNG")
# create a vehicle object with the name 'ego', vehicle model 'scintilla' and the vehicle version 'gtx'
ego = Vehicle('ego', model='scintilla', partConfig='vehicles/scintilla/gtx.pc', licence='HNU')

# add the created vehicle object 'ego' to the scenario at the specific location and rotation
scenario.add_vehicle(ego, pos=(245.11, -906.94, 247.46),
                     rot_quat=(0.0010, 0.1242, 0.9884, -0.0872))
                     
#scenario.add_vehicle(ego, pos=(0, 0, 0),
#                     rot_quat=(0.0010, 0.1242, 0.9884, -0.0872))
scenario.make(beamng)

# load and start the scenario
print (">>> load and start scenario + vehicle in BeamNG")
beamng.scenario.load(scenario)
beamng.scenario.start()

# attach a sensor that gathers information
electrics = Electrics()
ego.sensors.attach('electrics', electrics)

IMU = AdvancedIMU('accel1', beamng, ego, gfx_update_time=0.01)


# let AI drive the vehicle on road randomly
ego.control(gear=1)
ego.ai.set_mode('span')
ego.ai.drive_in_lane(True)


def process_connect2ServerHIVE():
    ##connect to MQTTServer:  
    print(">>>> start connect2 MQTT-Broker")
    mqttClient.connect("broker.hivemq.com", 1883, 60)
    mqttClient.loop_start()

#after connection was established 2
def on_connectHIVE(mqttClient2, userdata, flags, rc):
    print(">>>> connected to MQTT-Broker")
   
    

#Main-Program
print("START")
mqttClient = mqtt.Client()
mqttClient.on_connect = on_connectHIVE


#process_connect2ServerHIVE()

print ("START poll to read date from vehicle and publish to MQTT with topic 'uwc_beamng' every 2 seconds")
while True:
    # get new information from sensor
    ego.sensors.poll('electrics')
    
    data = IMU.poll() # Fetch the latest readings from the sensor.
    print("Position:", data[0]['pos'])
    
    # write updated information into variable
    vehicle_signals = ego.sensors['electrics']
    strJSON = str(vehicle_signals)
    strJSON = strJSON.replace('\'', '"')
    strJSON = strJSON.replace('False', 'false')
    strJSON = strJSON.replace('True', 'true')
    
    jsonObj = json.loads(strJSON);
    jsonObj['pos']=data[0]['pos'];
    
    #print(json.dumps(jsonObj))
    #mqttClient.publish('uwc_beamng', json.dumps(jsonObj))
   
    time.sleep(2)