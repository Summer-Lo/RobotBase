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
    value = int(veclocity)
    
    if(int(motorHandle) == int(hc.leftMotorHandle)):
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,int(hc.leftMotorVec+value), vrep.simx_opmode_oneshot)
        hc.leftMotorVec = int(hc.leftMotorVec+value)                    # update
    elif(int(motorHandle) == int(hc.rightMotorHandle)): 
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,int(hc.rightMotorVec+value), vrep.simx_opmode_oneshot)
        hc.rightMotorVec = int(hc.rightMotorVec+value)                  # update
    
    
# Rotate the ?th joint with ? angle (anti-clockwise)
def motorVeclocityNegative(handle, veclocity):
    global clientID
    motorHandle = int(handle)
    value = int(veclocity)
    
    if(int(motorHandle) == int(hc.leftMotorHandle)):
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,int(hc.leftMotorVec-value), vrep.simx_opmode_oneshot)
        hc.leftMotorVec = int(hc.leftMotorVec-value)                    # update
    elif(int(motorHandle) == int(hc.rightMotorHandle)):
        vrep.simxSetJointTargetVelocity(clientID, motorHandle,int(hc.rightMotorVec-value), vrep.simx_opmode_oneshot)
        hc.rightMotorVec = int(hc.rightMotorVec-value)                  # update

# Reset the current
def reset():
    global clientID
    vrep.simxSetJointTargetVelocity(clientID, hc.leftMotorHandle,0, vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetVelocity(clientID, hc.rightMotorHandle,0, vrep.simx_opmode_oneshot)

# Change the robot direction with negatice veclocity or positive veclocity
def changeDirection():
    global clientID
    leftVec = int(hc.leftMotorVec) * int(-1)
    rightVec = int(hc.rightMotorVec) * int(-1)
    vrep.simxSetJointTargetVelocity(clientID, hc.leftMotorHandle,int(leftVec), vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetVelocity(clientID, hc.rightMotorHandle,int(rightVec), vrep.simx_opmode_oneshot)



#testing
if __name__ == '__main__':
    time.sleep(0.1)
    motorVeclocityNegative(hc.leftMotorHandle,1)
    motorVeclocityNegative(hc.rightMotorHandle,1)
    #time.sleep(0.5)
    #changeDirection()
    #time.sleep(0.5)
    #reset()