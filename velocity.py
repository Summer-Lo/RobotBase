import numpy as np
import math
import time
import client_config as hc
import time
import vrep



RAD2DEG = 180 / math.pi
clientID = hc.clientID

def motorVeclocityPositive(handle, veclocity):
    global clientID
    motorHandle = int(handle)
    value = float(veclocity)
    print("Velocity is: ",value)
    
    if(int(motorHandle) == int(hc.leftMotorHandle)):
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,float(hc.leftMotorVec+value), vrep.simx_opmode_oneshot)
        hc.leftMotorVec = float(hc.leftMotorVec+value)                    # update
    elif(int(motorHandle) == int(hc.rightMotorHandle)): 
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,float(hc.rightMotorVec+value), vrep.simx_opmode_oneshot)
        hc.rightMotorVec = float(hc.rightMotorVec+value)                  # update
    
    
# Rotate the ?th joint with ? angle (anti-clockwise)
def motorVeclocityNegative(handle, veclocity):
    global clientID
    motorHandle = int(handle)
    value = float(veclocity)
    
    if(int(motorHandle) == int(hc.leftMotorHandle)):
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,float(hc.leftMotorVec-value), vrep.simx_opmode_oneshot)
        hc.leftMotorVec = float(hc.leftMotorVec-value)                    # update
    elif(int(motorHandle) == int(hc.rightMotorHandle)):
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,float(hc.rightMotorVec-value), vrep.simx_opmode_oneshot)
        hc.rightMotorVec = float(hc.rightMotorVec-value)                  # update

# Reset the current
def reset():
    global clientID
    vrep.simxSetJointTargetVelocity(clientID, hc.leftMotorHandle,0, vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetVelocity(clientID, hc.rightMotorHandle,0, vrep.simx_opmode_oneshot)
    hc.leftMotorVec = float(0)
    hc.rightMotorVec = float(0)

# Change the robot direction with negatice veclocity or positive veclocity
def changeDirection():
    global clientID
    leftVec = float(hc.leftMotorVec) * int(-1)
    rightVec = float(hc.rightMotorVec) * int(-1)
    vrep.simxSetJointTargetVelocity(clientID, hc.leftMotorHandle,float(leftVec), vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetVelocity(clientID, hc.rightMotorHandle,float(rightVec), vrep.simx_opmode_oneshot)
    hc.leftMotorVec = float(leftVec)
    hc.rightMotorVec = float(rightVec)


#testing
if __name__ == '__main__':
    time.sleep(0.1)
    motorVeclocityNegative(hc.leftMotorHandle,1)
    motorVeclocityNegative(hc.rightMotorHandle,1)
    #time.sleep(0.5)
    #changeDirection()
    #time.sleep(0.5)
    #reset()