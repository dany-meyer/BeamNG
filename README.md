# BeamNG

## Start Simulation via python:
python/bng_to_mqtt.py
- runs the simulation and puplish the data to HIVE-Broker

## Run MQTT-Bridge to CAN
- run the script mqtt_to_can.py on RaspPi
- the pi must be connected to Internet
- Use a running CAN-Application on the other end of VN 1610-Can-Adapter e.g. running CANoe-Simulation or running Simulink-Modell   
