import vrep
import sys
import numpy as np

# Object name for left side
robotName = "RobotBase"

# Object name for left side
leftMotorName = "RobotBase_leftMotor"
leftWheelFrontName = "RobotBase_leftWheel"
leftWheelBehindName = "RobotBase_leftWheelBehind"

# Object name for right side
rightMotorName = "RobotBase_rightMotor"
rightWheelFrontName = "RobotBase_rightWheel"
rightWheelBehindName = "RobotBase_rightWheelBehind"

# Object name for behind force sensor
leftForceSensorName = "RobotBase_leftJointBehind"
rightForceSensorName = "RobotBase_rightJointBehind"

# Start connection between VREP and Python API
print('Simulation started')

try:
    
    vrep.simxFinish(-1) #close the previous connections
    clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
    if clientID!=-1:
        print ('connect successfully')
    else:
        sys.exit("Error: no se puede conectar") #Terminar este script

except:
    print('Check if CoppeliaSim is open')

# Started connection
vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)     #Start simulation
print("-----------------Simulation start-----------------")


# Initization object handles
_, robotHandle = vrep.simxGetObjectHandle(clientID, robotName, vrep.simx_opmode_blocking)

_, leftMotorHandle = vrep.simxGetObjectHandle(clientID, leftMotorName, vrep.simx_opmode_blocking)
_, leftWheelFrontHandle = vrep.simxGetObjectHandle(clientID, leftWheelFrontName, vrep.simx_opmode_blocking)
_, leftWheelBehindHandle = vrep.simxGetObjectHandle(clientID, leftWheelBehindName, vrep.simx_opmode_blocking)

_, rightMotorHandle = vrep.simxGetObjectHandle(clientID, rightMotorName, vrep.simx_opmode_blocking)
_, rightWheelFrontHandle = vrep.simxGetObjectHandle(clientID, rightWheelFrontName, vrep.simx_opmode_blocking)
_, rightWheelBehindHandle = vrep.simxGetObjectHandle(clientID, rightWheelBehindName, vrep.simx_opmode_blocking)

_, leftForceSensorHandle = vrep.simxGetObjectHandle(clientID, leftForceSensorName, vrep.simx_opmode_blocking)
_, rightForceSensorHandle = vrep.simxGetObjectHandle(clientID, rightForceSensorName, vrep.simx_opmode_blocking)

# Print object handdles
objectHandle = {"RobotBase_leftMotor":leftMotorHandle,"RobotBase_leftWheel":leftWheelFrontHandle,"RobotBase_leftWheelBehind":leftWheelBehindHandle,"RobotBase_rightMotor":rightMotorHandle,"RobotBase_rightWheel":rightWheelFrontHandle,"RobotBase_rightWheelBehind":rightWheelBehindHandle}
key_list = list(objectHandle.keys())
val_list = list(objectHandle.values())
print("Key list of Object Handle: ",key_list)
print("Value list of Object Handle: ",val_list)

# Value Configuration
leftMotorVec = 0
rightMotorVec = 0
