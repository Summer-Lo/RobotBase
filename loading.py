import numpy as np
import math
import time
import client_config as hc
import time
import vrep
import sim



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def placeLoading():
    global clientID
    robotHandle = int(hc.robotHandle)
    loadingHandle = int(hc.loadingHandle)
    print(f"Current robot mass is: {hc.mass}")
    returnCode = 1
    while (returnCode!=0):
        returnCode, position = vrep.simxGetObjectPosition(clientID, int(robotHandle), -1, vrep.simx_opmode_blocking)
    returnCode = 1
    while (returnCode!=0):
        returnCode, orientation = vrep.simxGetObjectOrientation(clientID, int(robotHandle), -1, vrep.simx_opmode_blocking)
    for i in range(1,41):
        if (float(hc.mass) <= 10):
            position[2] = -1
        elif (float(hc.mass) > i * 10 and float(hc.mass) <= i*10+10):
            #position[2] = ((i-1)*0.003)+0.068
            position[2] = position[2] + 0.008 + ((i-1)*0.003)
        elif (float(hc.mass) > 400):
            return

    _ = vrep.simxSetObjectPosition(clientID, int(loadingHandle), -1, position, vrep.simx_opmode_blocking)
    _ = vrep.simxSetObjectOrientation(clientID, int(loadingHandle), -1, orientation, vrep.simx_opmode_blocking)

def scaleLoading():
    global clientID
    #value = (0.4-0.1)/(100-10)
    print(f"Current mass is: {hc.mass}")
    for i in range(1,41):
        if (float(hc.mass) <= 10):
            value = 0.005
        elif (float(hc.mass) > i * 10 and float(hc.mass) <= i*10+10):
            value = (i+1)*0.005
        elif (float(hc.mass) > 400):
            return

    factor = float(value) / float(hc.loadingScale)
    print(f"Value is : {value} Factor is: {factor}")
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'scaleLoading',[],[factor],[],b'',vrep.simx_opmode_blocking)
    result = float(hc.loadingScale) * float(factor)
    hc.loadingScale = float(result)
    print(f"The current width of robot is: {float(hc.loadingScale)}")
    return result
    
    # loading information
    # Z value and Z position
    # 0.1----------0.1050
    # 0.09----------0.1
    # 0.08----------0.095
    # 0.07----------0.9
    # 0.06----------0.085
    # 0.05----------0.08
    # 0.04----------0.075
    # 0.03----------0.07
    # 0.02----------0.065
    # 0.01----------0.06

    # loading information
    # Z value and Z position
    # 0.005----------0.068
    # 0.01----------0.071
    # 0.015----------0.074
    # 0.02----------0.77
    # 0.025----------0.08
    # 0.03----------0.083
    # 0.04----------0.075
    # 0.03----------0.07
    # 0.02----------0.065
    # 0.01----------0.06





#testing
if __name__ == '__main__':
    setRobotMass()
    scaleRobot()


