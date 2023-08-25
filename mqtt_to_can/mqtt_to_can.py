# Bridge from MQTT to CAN-Bus using in RaspPi

import can
import os
import time

import sys
import struct
import socket
import os

import paho.mqtt.client as mqtt
from time import sleep
import threading
import time
import json

pid_mapping = {
    5 : "oil_temperature",
    12 : "rpm",
    13 : "wheelspeed"
    }
values = {
    "oil_temperature" : {"value": None, "sended": False},
    "rpm" : {"value": None, "sended": False},
    "wheelspeed" : {"value": None, "sended": False}
    }


topic_str = "uwc_beamng"
receivedData = False


os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)



######## MQTT callback-methods ##################################
def process_connect2ServerHIVE():
    ##connect to MQTTServer:  
    print("start connect2")
    mqttClient2.connect("broker.hivemq.com", 1883, 60)
    mqttClient2.loop_start()
    
#after connection was established 2
def on_connectHIVE(mqttClient2, userdata, flags, rc):
    print("connected to HIVE")
    mqttClient2.subscribe(topic_str, 0)
    print("subscribed for topic on HIVE: ", topic_str)
    
    
#Reseive message and send with latence a response
def on_messageHIVE(mosq, obj, msg):
    global receivedData, values, value_sended
    try:
        if msg.topic.startswith(topic_str):
            receivedData = True
            
            m_decode = str(msg.payload.decode("utf-8","ignore"))
            m_decode = m_decode.replace('\'', '"')
            m_decode = m_decode.replace('False', 'false')
            m_decode = m_decode.replace('True', 'true')
    
            #print(m_decode)
            m_in = json.loads(m_decode)
            
            
            values["wheelspeed"]["value"]=m_in["wheelspeed"]*3.6
            values["wheelspeed"]["sended"]=False
            
            values["rpm"]["value"]=m_in["rpm"]
            values["rpm"]["sended"]=False
            
            values["oil_temperature"]["value"]=m_in["oil_temperature"]
            values["oil_temperature"]["sended"]=False
            
      
    except:
        print("Fehler")


########### Can-Message received ########################################################
def on_message_received(msg):
    
    global receivedData, values, value_sended
    if (msg.arbitration_id == 0x7df):
        
        if receivedData==False:
            print("Received can-request, no Data from Broker yet --> no answer to can bus")
        
        else:
            pid = msg.data[2]
            pci = -1
            valName = pid_mapping[pid]
            val=values[valName]["value"]
            valSended = values[valName]["sended"]
            
            if valSended == False:
                print("OBD Anfrage erhalten ", valName, " ", val)
                 
                if (pid == 5):
                    transferValue = int(val)+40
                    A = transferValue
                    B = 0
                    pci=3
                    
                elif (pid == 12):
                    transferValue = int(val * 4)
                    A = int(transferValue/256)
                    B = transferValue%256
                    pci=4
                    
                elif (pid == 13):
                    A = int(val)
                    B = 0
                    pci = 3
                    
            if (pci!=-1):
                data2 = [pci, 0x41, pid, A, B, 0, 0, 0]
                msg_back = can.Message(arbitration_id=0x7e8, data=data2, extended_id=False)
                bus.send(msg_back)
                values[valName]["sended"]=True;
                

bus = can.ThreadSafeBus(channel='can0', bustype='socketcan_native')
msg = can.Message(arbitration_id=0x050, data=[1], extended_id=False)
bus.send(msg)

listener = can.Listener()
listener.on_message_received = on_message_received
notifier = can.Notifier(bus, [listener])


print("START")
mqttClient2 = mqtt.Client()
mqttClient2.on_connect = on_connectHIVE
mqttClient2.on_message = on_messageHIVE


process_connect2ServerHIVE()

while True:
    time.sleep(2)
    if receivedData:
        print (values["oil_temperature"]["value"], " ",
               values["rpm"]["value"], " ",
               values["wheelspeed"]["value"])
    








