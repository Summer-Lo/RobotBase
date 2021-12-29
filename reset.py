import numpy as np
import math
import time
import client_config as hc
import time
import vrep
import velocity



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def resetRobot():
    global clientID
    robotPos = [float(hc.robotPosX),float(hc.robotPosY),float(hc.robotPosZ)]
    robotOri = [float(float(hc.robotAlpha)/RAD2DEG),float(float(hc.robotBeta)/RAD2DEG),float(float(hc.robotGamma)/RAD2DEG)]
    #print(robotPos)
    returnCode = 1
    while (returnCode!=0):
        returnCode = vrep.simxSetObjectPosition(clientID, int(hc.robotHandle), -1, robotPos, vrep.simx_opmode_blocking)
    returnCode = 1
    while (returnCode!=0):
        returnCode = vrep.simxSetObjectOrientation(clientID, int(hc.robotHandle), -1, robotOri, vrep.simx_opmode_blocking)


def resetJoint():
    global clientID
    for i in range(len(hc.jointHandle)):
        jointPos = [float(hc.jointPosX[i]),float(hc.jointPosY[i]),float(hc.jointPosZ[i])]
        jointOri = [float(float(hc.jointAlpha[i])/RAD2DEG),float(float(hc.jointBeta[i])/RAD2DEG),float(float(hc.jointGamma[i])/RAD2DEG)]
        returnCode = 1
        while (returnCode!=0):
            returnCode = vrep.simxSetObjectPosition(clientID, int(hc.jointHandle[i]), -1, jointPos, vrep.simx_opmode_blocking)
        returnCode = 1
        while (returnCode!=0):
            returnCode = vrep.simxSetObjectOrientation(clientID, int(hc.jointHandle[i]), -1, jointOri, vrep.simx_opmode_blocking)

def resetWheel():
    global clientID
    for i in range(len(hc.wheelHandle)):
        wheelPos = [float(hc.wheelPosX[i]),float(hc.wheelPosY[i]),float(hc.wheelPosZ[i])]
        wheelOri = [float(float(hc.wheelAlpha[i])/RAD2DEG),float(float(hc.wheelBeta[i])/RAD2DEG),float(float(hc.wheelGamma[i])/RAD2DEG)]
        returnCode = 1
        while (returnCode!=0):
            returnCode = vrep.simxSetObjectPosition(clientID, int(hc.wheelHandle[i]), -1, wheelPos, vrep.simx_opmode_blocking)
        returnCode = 1
        while (returnCode!=0):
            returnCode = vrep.simxSetObjectOrientation(clientID, int(hc.wheelHandle[i]), -1, wheelOri, vrep.simx_opmode_blocking)

def resetRobotMass(handle, value):
    global clientID
    Handle = int(handle)
    #res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
        #vrep.sim_scripttype_childscript,'rg2Open',[],[],[],b'',vrep.simx_opmode_blocking)
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'massReset',[],[value],[],b'',vrep.simx_opmode_blocking)
    return retFloats

def resetWheelSize():
    global clientID
    value = 0.06
    factor = float(value) / float(hc.wheelScale)
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'scaleReset',[],[factor],[],b'',vrep.simx_opmode_blocking)
    result = float(hc.wheelScale) * float(factor)
    hc.wheelScale = float(result)
    print(f"The current radius of wheels are: {float(hc.wheelScale)}")
    return result

def resetGraph():
    global clientID
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'resetGraph',[],[],[],b'',vrep.simx_opmode_blocking)

def run():
    _ = vrep.simxPauseSimulation(clientID,vrep.simx_opmode_blocking)
    time.sleep(0.3)
    velocity.reset()
    resetRobotMass(int(hc.robotHandle),10)
    resetRobot()
    time.sleep(0.1)
    resetJoint()
    time.sleep(0.1)
    resetWheel()
    time.sleep(0.1)
    resetWheelSize()
    time.sleep(0.3)
    _ = vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)

#testing
if __name__ == '__main__':
    run()


