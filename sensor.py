import numpy as np
import math
import time
import client_config as hc
import time
import vrep



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def getForceSensor(handle):
    global clientID
    forceSensorHandle = int(handle)
    returnCode = 1
    while(returnCode != 0):
        returnCode, state, forceVector, torqueVector = vrep.simxReadForceSensor(clientID, forceSensorHandle, vrep.simx_opmode_oneshot)
    return returnCode, state, forceVector, torqueVector

def getObjectVelocity(handle):
    global clientID
    objectHandle = int(handle)
    returnCode, linearVec, angularVec = vrep.simxGetObjectVelocity(clientID, objectHandle, vrep.simx_opmode_oneshot)
    return returnCode, linearVec, angularVec




#testing
if __name__ == '__main__':
    while True:
        returnCode, state, forceVector, torqueVector = getForceSensor(hc.leftForceSensorHandle)
        print("----------Left Force Sensor result----------")
        print(f"Return Code is {returnCode}")
        print(f"Force Sensor State is {state}")
        print(f"Force Vector is {forceVector}")
        print(f"Torque Vector is {torqueVector}")
        time.sleep(1)
        returnCode, state, forceVector, torqueVector = getForceSensor(hc.rightForceSensorHandle)
        print("----------Right Force Sensor result----------")
        print(f"Return Code is {returnCode}")
        print(f"Force Sensor State is {state}")
        print(f"Force Vector is {forceVector}")
        print(f"Torque Vector is {torqueVector}")
        time.sleep(1)

