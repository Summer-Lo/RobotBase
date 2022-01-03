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
            position[2] = ((i-1)*0.003)+0.068
        elif (float(hc.mass) > 400):
            return
    '''
    if (float(hc.mass) == 10):
        position[2] = float(-1)
    elif (float(hc.mass) > 10 and float(hc.mass) <= 20):
        position[2] = float(0.042)
    elif (float(hc.mass) > 20 and float(hc.mass) <= 30):
        position[2] = float(0.047)
    elif (float(hc.mass) > 30 and float(hc.mass) <= 40):
        position[2] = float(0.052)
    elif (float(hc.mass) > 40 and float(hc.mass) <= 50):
        position[2] = float(0.057)
    elif (float(hc.mass) > 50 and float(hc.mass) <= 60):
        position[2] = float(0.062)
    elif (float(hc.mass) > 60 and float(hc.mass) <= 70):
        position[2] = float(0.067)
    elif (float(hc.mass) > 70 and float(hc.mass) <= 80):
        position[2] = float(0.072)
    elif (float(hc.mass) > 80 and float(hc.mass) <= 90):
        position[2] = float(0.077)
    elif (float(hc.mass) > 90 and float(hc.mass) <= 100):
        position[2] = float(0.082)
    else:
        return
    '''
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
    '''
    if (float(hc.mass) == 10):
        value = 0.01
    elif (float(hc.mass) > 10 and float(hc.mass) <= 20):
        value = 0.02
    elif (float(hc.mass) > 20 and float(hc.mass) <= 30):
        value = 0.03
    elif (float(hc.mass) > 30 and float(hc.mass) <= 40):
        value = 0.04
    elif (float(hc.mass) > 40 and float(hc.mass) <= 50):
        value = 0.05
    elif (float(hc.mass) > 50 and float(hc.mass) <= 60):
        value = 0.06
    elif (float(hc.mass) > 60 and float(hc.mass) <= 70):
        value = 0.07
    elif (float(hc.mass) > 70 and float(hc.mass) <= 80):
        value = 0.08
    elif (float(hc.mass) > 80 and float(hc.mass) <= 90):
        value = 0.09
    elif (float(hc.mass) > 90 and float(hc.mass) <= 100):
        value = 0.1
    else:
        return
    '''    
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


