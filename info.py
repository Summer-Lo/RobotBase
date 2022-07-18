import numpy as np
import math
import time
import client_config as hc
import time
import vrep
import sim



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def getMotorTorque(handle):
    global clientID
    motorHandle = int(handle)
    returnCode, value = vrep.simxGetJointForce(clientID, motorHandle, vrep.simx_opmode_oneshot)
    return value

def getMotorMaxTorque(handle):
    global clientID
    motorHandle = int(handle)
    _,motorMaxTorque = sim.simxGetJointMaxForce(clientID, motorHandle,vrep.simx_opmode_blocking)
    return motorMaxTorque

def getObjectVelocity(handle):
    global clientID
    objectHandle = int(handle)
    returnCode, linearVec, angularVec = vrep.simxGetObjectVelocity(clientID, objectHandle, vrep.simx_opmode_oneshot)
    return returnCode, linearVec, angularVec

def readRobotMass():
    global clientID
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
    vrep.sim_scripttype_childscript,'readMass',[],[],[],b'',vrep.simx_opmode_blocking)
    print(f"RES is: {res}")
    print(f"Result in Read Robot Mass is : {retFloats}")
    if not retFloats:
        print(f"Not resFloats!")
        retFloats = [0]
        res = 1
        return res,retFloats[0]
    else:
        return res,retFloats[0]


#testing
if __name__ == '__main__':
    while True:
        result, linear, angular = getObjectVelocity(hc.robotHandle)
        print(f"result is {result}")
        print(linear)
        print(angular)
        time.sleep(1)

