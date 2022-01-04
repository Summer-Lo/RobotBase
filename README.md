# RobotBase
A simulation for testing the robot performance with different velocity, toque, mass, and wheel configurations.

## For Window User
You may use anaconda to create a virtual environment to execute a Python program.

## Coppliasim Scene Version
- RobotBase_v4.ttt for **mini moblie robot**

- RobotBase_v5.ttt for **IC382 Robot**

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
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/anconda_environment.png)

Step 5: Input the necessary information (Input Name and select Python version 3.8)

Step 6: Click "Create" to complete environment creation [Green]
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/anconda_environmentCreate.png)

### 2.2. Install Python library
Step 1: Switch the filter to "All" to display all library

Step 2: Search the following library name

Step 3: Click the left triangle for downloading

Step 4: Repeat  Step 2 & Step 3 to install the following libraries
```
mpmath
```
```
numpy
```
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/anconda_mpmath.png)
Step 5: Click "Apply" to download selected library [Blue][Purple]
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/anconda_library.png)

Step 6: Run the terminal with the created environment [Red]
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/anconda_terminal.png)

Step 7: Type the following command to download pygame and pygame-gui
```
pip install pygame-gui
```

## 3. Program execution
Step 1: Open CoppliaSim with the "RobotBase_v5.ttt" scene

Step 2: Open the terminal with the created environment

Step 3: Change the directory by typing the following command with changing {your file directory}
```
cd /D {Inout_Your_Folder_Path}
```
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/anconda_filePath.png)
Step 4: Type the following command to execute the program
```
python robotBase.py
```

Remark: Please make sure that the terminal opened inside your anaconda environment. You can see that it will display your environment name in each row header.

## 4. Control Panel
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/panel_interface.png)

[Red]: Motors angular velocity control (-0.5, -0.1, +0.1, +0.5 rad/s)

[Orange]: Robot movement control

- Forward/Backward: change the robot direction

- Set Velocity: Input value of motors' positive angular velocity (rad/s) for driving the robot forward or negative angular velocity (rad/s) for driving backward

- Reset Velocity: Reset the robot velocity to become 0 rad/s (stop)

[Yellow]: Mass (kg)  configuration (Remark: keep robot mass in range of 10 -  400kg)

- Mass Increase: Increase the robot mass with 10 kg

- Mass Decrease: Decrease the robot mass with 10 kg

- Mass Config: Input value for configurating the robot mass



[Green]: Motor Max Torque and Wheel Configuration (Max Torque and Wheel diameter)

- Set Motor Max Torque: Input the value (Nm) for configurating the motors' max torque

- Wheel Dimension: Input the wheel dimension (m) for modifying the size of robot's wheels

[Blue]: Robot information (Mass and Wheel diameter)

[Purple]: Robot linear and angular Velocity

[Gray]: Motors' Torque

## 5. Observation
- There are some graphs that display the data for selecting the motor

- Red for the left motor

- Blue for the right motor

![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/interface.png)

### 1. MotorVelocity (Degrees/Seconds)      --Hided--
This graph shows the motors' angular velocity with the time changed. 

### 2. MotorTorque (kg*m^2/s^2)     --Hided--
This graph shows the motors' torque with the time changed. 

### 3. WheelAngularVelocity (Degrees/Seconds)       --Hided--
This graph shows the front Wheels' angular velocity with the time changed. 

### 4. Graph (x:Degrees/Seconds)(y:kg*m^2/s^2)
This graph shows the relationship between the motors' angular velocity and torque.

The X-axis for angular velocity

The Y-axis for torque

### 5. linearVelocity (Meters/Seconds)
This graph shows the robot's linear velocity with the time changed. 

## 6. Demonstration

### 6.1. Basic Control
This video shows the basic movement of the robot. The action involved in this demonstration which includes ">> (R)", ">> (F)", "Forward/Backward", "Set Velocity", and "Reset Velocity"
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/robotMovement.gif)

### 6.2. Reset Function
This video shows the "Reset" function which will be operated automatically before stopping the program. Also, the "Reset Robot" button is provided to use this function.
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/reset.gif)

### 6.3. Mass Configuration
This video shows the configuration of robot mass during the simulation running. When the robot mass is changing, the thickness of loading will be changed according to the robot mass. The action involved in this demonstration includes "Mass Increase", "Mass Decrease", and "Mass Config".
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/mass.gif)

### 6.4. Motor Max Torque Configuration
This video shows the "Set Motor Max Torque" function which can limit the motor torque. 
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/maxTorque.gif)

### 6.5. Wheel Dimension Configuration
This video shows the "Wheel Dimension" function which configurate the wheel diameter (m).
![image](https://github.com/Summer-Lo/RobotBase/blob/linux_v4.2.0/robotBase_image/wheelConfig.gif)



