import numpy as np
import math
import time
import client_config as hc
import time
import vrep
import sim



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def updateRobotMass(handle, value):
    global clientID
    Handle = int(handle)
    #res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
        #vrep.sim_scripttype_childscript,'rg2Open',[],[],[],b'',vrep.simx_opmode_blocking)
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'massModify',[],[value],[],b'',vrep.simx_opmode_blocking)
    hc.mass = float(retFloats[0])
    return retFloats[0]

def setRobotMass():
    global clientID
    value = float(hc.userInput)
    #value = float(input("Please input the robot mass (kg): "))
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'setMass',[],[value],[],b'',vrep.simx_opmode_blocking)
    print(f"Current robot mass is : {retFloats} kg")
    hc.mass = float(retFloats[0])
    return retFloats[0]

def scaleRobot():
    global clientID
    #value = (0.4-0.1)/(100-10)
    print(f"Current mass is: {hc.mass} kg")
    if (float(hc.mass) == 10):
        value = 0.01
    elif (float(hc.mass) >= 11 and float(hc.mass) <= 20):
        value = 0.0135
    elif (float(hc.mass) >= 21 and float(hc.mass) <= 30):
        value = 0.017
    elif (float(hc.mass) >= 31 and float(hc.mass) <= 40):
        value = 0.0205
    elif (float(hc.mass) >= 41 and float(hc.mass) <= 50):
        value = 0.024
    elif (float(hc.mass) >= 51 and float(hc.mass) <= 60):
        value = 0.0275
    elif (float(hc.mass) >= 61 and float(hc.mass) <= 70):
        value = 0.031
    elif (float(hc.mass) >= 71 and float(hc.mass) <= 80):
        value = 0.0345
    elif (float(hc.mass) >= 81 and float(hc.mass) <= 90):
        value = 0.038
    elif (float(hc.mass) >= 91 and float(hc.mass) <= 100):
        value = 0.042
    factor = float(value) / float(hc.robotScale)
    print(f"Value is : {value}Factor is: {factor}")
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'scaleLoading',[],[factor],[],b'',vrep.simx_opmode_blocking)
    result = float(hc.robotScale) * float(factor)
    hc.robotScale = float(result)
    print(f"The current width of robot is: {float(hc.robotScale)}")
    return result

def scaleWheel():           # only allow 0.01-0.04
    global clientID
    value = float(hc.userInput)
    #value = float(input("Please input the diameter of Wheels (m): "))
    factor = float(value) / float(hc.wheelScale)
    #factor = float(float(factor)/10)
    res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, hc.robotName,\
        vrep.sim_scripttype_childscript,'scaleWheel',[],[factor],[],b'',vrep.simx_opmode_blocking)
    result = float(hc.wheelScale) * float(factor)
    hc.wheelScale = float(result)
    print(f"The current diameter of wheels are : {float(hc.wheelScale)} m")
    return result

def updateJointMaxTorque():
    global clientID
    maxTorque = float(hc.userInput)
    #maxTorque = float(input("Please input the max torque of two motors (Nm): "))
    sim.simxSetJointMaxForce(clientID, hc.leftMotorHandle,maxTorque,vrep.simx_opmode_blocking)
    sim.simxSetJointMaxForce(clientID, hc.rightMotorHandle,maxTorque,vrep.simx_opmode_blocking)
    _,leftMotorMaxTorque = sim.simxGetJointMaxForce(clientID, hc.leftMotorHandle,vrep.simx_opmode_blocking)
    _,rightMotorMaxTorque = sim.simxGetJointMaxForce(clientID, hc.rightMotorHandle,vrep.simx_opmode_blocking)
    print(f"Current left motor max torque is {leftMotorMaxTorque} Nm")
    print(f"Current right motor max torque is {rightMotorMaxTorque} Nm")

#testing
if __name__ == '__main__':
    setRobotMass()
    scaleRobot()


