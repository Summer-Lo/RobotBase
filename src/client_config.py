import vrep
import sys
import numpy as np

# Object name for left side
robotName = "RobotBase"
loadingName = "loading"

# Object name for left side
leftMotorName = "RobotBase_leftMotor"
leftJointBehindName = "RobotBase_leftJointBehind"
leftWheelFrontName = "RobotBase_leftWheel"
leftWheelBehindName = "RobotBase_leftWheelBehind"

# Object name for right side
rightMotorName = "RobotBase_rightMotor"
rightJointBehindName = "RobotBase_rightJointBehind"
rightWheelFrontName = "RobotBase_rightWheel"
rightWheelBehindName = "RobotBase_rightWheelBehind"

# camera
cameraName = "DefaultCamera"

# Object name for behind force sensor
#leftForceSensorName = "RobotBase_leftJointBehind"
#rightForceSensorName = "RobotBase_rightJointBehind"

# Start connection between VREP and Python API
print('Simulation started')

try:
    
    vrep.simxFinish(-1) #close the previous connections
    clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
    print(f"Client ID is: {clientID}")
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
_, loadingHandle = vrep.simxGetObjectHandle(clientID, loadingName, vrep.simx_opmode_blocking)

_, leftMotorHandle = vrep.simxGetObjectHandle(clientID, leftMotorName, vrep.simx_opmode_blocking)
_, leftJointBehindHandle = vrep.simxGetObjectHandle(clientID, leftJointBehindName, vrep.simx_opmode_blocking)
_, leftWheelFrontHandle = vrep.simxGetObjectHandle(clientID, leftWheelFrontName, vrep.simx_opmode_blocking)
_, leftWheelBehindHandle = vrep.simxGetObjectHandle(clientID, leftWheelBehindName, vrep.simx_opmode_blocking)

_, rightMotorHandle = vrep.simxGetObjectHandle(clientID, rightMotorName, vrep.simx_opmode_blocking)
_, rightJointBehindHandle = vrep.simxGetObjectHandle(clientID, rightJointBehindName, vrep.simx_opmode_blocking)
_, rightWheelFrontHandle = vrep.simxGetObjectHandle(clientID, rightWheelFrontName, vrep.simx_opmode_blocking)
_, rightWheelBehindHandle = vrep.simxGetObjectHandle(clientID, rightWheelBehindName, vrep.simx_opmode_blocking)

wheelHandle = [int(leftWheelFrontHandle),int(rightWheelFrontHandle),int(leftWheelBehindHandle),int(rightWheelBehindHandle)]
jointHandle = [int(leftMotorHandle),int(rightMotorHandle),int(leftJointBehindHandle),int(rightJointBehindHandle)]

_, cameraHandle = vrep.simxGetObjectHandle(clientID, cameraName, vrep.simx_opmode_blocking)

# Print object handdles
objectHandle = {"RobotBase_leftMotor":leftMotorHandle,"RobotBase_leftWheel":leftWheelFrontHandle,"RobotBase_leftWheelBehind":leftWheelBehindHandle,"RobotBase_rightMotor":rightMotorHandle,"RobotBase_rightWheel":rightWheelFrontHandle,"RobotBase_rightWheelBehind":rightWheelBehindHandle}
key_list = list(objectHandle.keys())
val_list = list(objectHandle.values())
print("Key list of Object Handle: ",key_list)
print("Value list of Object Handle: ",val_list)

# Value Configuration
leftMotorVec = 0
rightMotorVec = 0

#Robot Configuration
robotScale = 0.01
mass = 10   #kg
loadingScale = 0.005

# Wheel Configuration
wheelScale = 0.12

# orginal position and orientation (for IC382)
# wheel = [leftWheel, rightWheel, leftWheelBehind, rightWheelBehind]
wheelPosX = [-0.33,0.33,-0.33,0.33]
wheelPosY = [0.4,0.4,-0.4,-0.4]
wheelPosZ = [0.0595,0.05945,0.06,0.06]
wheelAlpha = [0,0,0,0]
wheelBeta = [-90,-90,-90,-90]
wheelGamma = [-90,-90,-90,-90]

# Joint = [leftMotor, rightMotor, leftJointBehind, rightJointBehind]
jointPosX = [-0.31,0.31,-0.31,0.31]
jointPosY = [0.4,0.4,-0.4,-0.4]
jointPosZ = [0.0595,0.05945,0.06,0.06]
jointAlpha = [0,0,0,0]
jointBeta = [-90,-90,-90,-90]
jointGamma = [90,90,90,90]

# Robot
robotPosX = 0
robotPosY = 0
robotPosZ = 0.06
robotAlpha = 0
robotBeta = 0
robotGamma = 180

# Pause or resume status
pauseOrResume = 0

# camera default position
cameraHome = [-0.0044875,-7.1338,30.797,-167,0,-180]

# User input
userInput = ""

# function status = [{Set Velocity},{Mass Configuration},{Set Max Torque},{Set Wheel Size}]
functionStatus = [0,0,0,0]

# question for asking user input
question = ""
inputHeading = ""