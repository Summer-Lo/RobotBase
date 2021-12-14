import numpy as np
import math
import time
import client_config as hc
import time
import vrep



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def getMotorTorque(handle):
    global clientID
    motorHandle = int(handle)
    result, value = vrep.simxGetJointForce(clientID, motorHandle, vrep.simx_opmode_oneshot)
    return value

def getObjectVelocity(handle):
    global clientID
    objectHandle = int(handle)
    result, linearVec, angularVec = vrep.simxGetObjectVelocity(clientID, objectHandle, vrep.simx_opmode_oneshot)
    return result, linearVec, angularVec
    



#testing
if __name__ == '__main__':
    while True:
        result, linear, angular = getObjectVelocity(hc.robotHandle)
        print(linear)
        print(angular)
        time.sleep(1)

