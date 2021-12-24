# RobotBase
A simulation for testing the robot performance with different velocity, toque, mass, wheel configuration.

## 1. Software installation
### 1.1. CoppliaSim v4.2.0 (Edu)
installation link
```
https://coppeliarobotics.com/downloads
```

### 1.2. Anaconda
installation link

```
https://www.anaconda.com/products/individual
```
For reference
```
https://medium.com/python4u/anaconda%E4%BB%8B%E7%B4%B9%E5%8F%8A%E5%AE%89%E8%A3%9D%E6%95%99%E5%AD%B8-f7dae6454ab6
```

## 2. Python Virtual Environment
### 2.1. Environment Creation
Step 1: Download & Installation Anaconda

Step 2: Launch Anaconda (remark: please don't update anaconda version)

Step 3: Click the "Environments" button on the left side [Orange]

Step 4: Click the the "Create" button on the left-bottom conern [Red]

Step 5: Input the necessary information (Input Name and select Python version 3.8)

Step 6: Click "Create" to complete environment creation

### 2.2. Install Python library
Step 1: Switch the filter to "All" for display all library

Step 2: Search the following library name

Step 3: Click the left trangle for downloading

Step 4: Repeat the Step 2 & Step 3 for install the following library\
```
mpmath
```
```
numpy
```

Step 5: Click "Apply" to download selected library [Blue][Purple]

Step 6: Run the terminal with the created environment [Red]

Step 7: Type the following command to download pygame and pygame-gui
```
pip install pygame-gui
```

## 3. Program execution
Step 1: Open CoppliaSim with the "RobotBase_v4.ttt" scene

Step 2: Open the terminal with the created environment

Step 3: Change the directory by typing following command with changing {your file directory}
```
cd /D {Inout_Your_Folder_Path}
```

Step 4: Type the following command to execute the program
```
python robotBase.py
```

Remark: Please make sure that the terminal opened inside your anaconda environment. You can see that it will display your environment name in each row header.

## 4. Control Panel
[Red]: Motors angular velocity control (-0.5, -0.1, +0.1, +0.5 rad/s)

[Orange]: Robot movement control

- Forward/Backward: change the robot direction

- Set Velocity: Input value of motors' angular velocity (rad/s) for diriving the robot forward

- Reset Velocity: Reset the robot velocity to become 0 rad/s (stop)

[Yellow]: Mass (kg) and wheel dimension (m) configuration

- Mass Increase: Increase the robot mass with 10 kg

- Mass Decrease: Decrease the robot mass with 10 kg

- Wheel Dimension: Change the Wheel dimension (m) with input at terminal

[Green]: Robot information (Mass and Wheel diameter)

[Blue]: Robot linear and angular Velocity

[Purple]: Motors' Torque

## 5. Observation
There are some graphs which display the data for selecting the motor

Red for left motor

Blue for right motor

### 1. MotorVelocity (Degrees/Seconds)
This graph shows the motors' angular velocity with the time changed. 

### 2. MotorTorque (kg*m^2/s^2)
This graph shows the motors' torque with the time changed. 

### 3. WheelAngularVelocity (Degrees/Seconds)
This graph shows the front Wheels' angular velocity with the time changed. 

### 4. Graph (x:Degrees/Seconds)(y:kg*m^2/s^2)
This graph shows the relationship between the motors' angular velocity and torque.

X-axis for angular velocity

Y-axis for torque

### 5. linearVelocity (Meters/Seconds)
This graph shows the robot linear velocity with the time changed. 


