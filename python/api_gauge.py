import sys
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import (IMU, Camera, Damage, Electrics, Lidar, State, Timer, Ultrasonic)

# open BeamNG at it's location
beamng = BeamNGpy('localhost', 64256, home='C:\BeamNG\BeamNG.tech.v0.28.1.0')
beamng.open()

# create a scenario with the map 'gridmap' and name the scenario 'Car IT'
scenario = Scenario('smallgrid', 'Car IT')

# create a vehicle object with the name 'ego', vehicle model 'scintilla' and the vehicle version 'gtx'
ego = Vehicle('ego', model='scintilla', partConfig='vehicles/scintilla/gtx.pc', licence='HNU')

# add the created vehicle object 'ego' to the scenario at the specific location and rotation
scenario.add_vehicle(ego, pos=(0, 0, 0), rot_quat=(0, 0, 0, 1))
scenario.make(beamng)

# load and start the scenario
beamng.scenario.load(scenario)
beamng.scenario.start()

# attach a sensor that gathers information
electrics = Electrics()
ego.sensors.attach('electrics', electrics)

# let AI drive the vehicle on road randomly
#ego.control(gear=1)
#ego.ai.set_mode('span')
#ego.ai.drive_in_lane(True)

while True:
    # get new information from sensor
    ego.sensors.poll('electrics')

    # write updated information into variable
    vehicle_signals = ego.sensors['electrics']

    # get velocity from signal list and convert m/s to km/h
    velocity = vehicle_signals['wheelspeed'] * 3.6

    # get rpm from signal list
    rpm = vehicle_signals['rpm']
    
    # output velocity and rpm in console
    sys.stdout.write("%d km/h   ".center(15) % (velocity))
    sys.stdout.write("%d rpm \r" % (rpm))
    sys.stdout.flush()