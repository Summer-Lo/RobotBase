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






#testing
if __name__ == '__main__':
    while True:
        result = updateRobotMass(hc.robotHandle,10)
        print(f"Result is: {result}")
        time.sleep(5)
        result = updateRobotMass(hc.robotHandle,-10)
        print(f"Result is: {result}")

