import numpy as np
import math
import time
import client_config as hc
import time
import vrep



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def updateRobotMass(handle, value):
    global clientID
    Handle = int(handle)
    #res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
        #vrep.sim_scripttype_childscript,'rg2Open',[],[],[],b'',vrep.simx_opmode_blocking)
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'massModify',[],[value],[],b'',vrep.simx_opmode_blocking)
    return retFloats

def scaleWheel():
    global clientID
    value = input("Please input the radius of Wheels: ")
    factor = float(value) / float(hc.wheelScale)
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'scaleWheel',[],[factor],[],b'',vrep.simx_opmode_blocking)
    result = float(hc.wheelScale) * float(factor)
    hc.wheelScale = float(result)
    print(f"The current radius of wheels are: {float(hc.wheelScale)}")
    return result


#testing
if __name__ == '__main__':
    while True:
        result = scaleWheel()


