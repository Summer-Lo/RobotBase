#-*- coding:utf-8 -*-

"""
keyboard Instructions:
    robot moving velocity: <=5(advise)
    Q,W: joint 0
    A,S: joint 1
    Z,X: joint 2
    E,R: joint 3
    D,F: joint 4
    C,V: joint 5
    P: exit()
    T: close RG2
    Y: open RG2
"""

import sys
import math
import time
import pygame
import pygame_gui
import vrep
import client_config as hc
import velocity
import info
import sensor
import modify
import reset
import loading
import threading

class robotBase:

    # communication and read the handles
    def __init__(self):
        self.clientID = hc.clientID
        # Left Side Object
        self.leftMotorHandle = hc.leftMotorHandle
        self.leftWheelFrontHandle = hc.leftWheelFrontHandle
        self.leftWheelBehindHandle = hc.leftWheelBehindHandle
        # Right Side Object
        self.rightMotorHandle = hc.rightMotorHandle
        self.rightWheelFrontHandle = hc.rightWheelFrontHandle
        self.rightWheelBehindHandle = hc.rightWheelBehindHandle

    # disconnect
    def __del__(self):
        clientID = self.clientID
        vrep.simxFinish(clientID)
        print('Simulation end')
        
    # show Handles information
    def showHandles(self):
        clientID = self.clientID
        # Left
        leftMotorHandle = self.leftMotorHandle
        leftWheelFrontHandle = self.leftWheelFrontHandle
        leftWheelBehindHandle = self.leftWheelBehindHandle
        # Right
        rightMotorHandle = self.rightMotorHandle
        rightWheelFrontHandle = self.rightWheelFrontHandle
        rightWheelBehindHandle = self.rightWheelBehindHandle
        
        print('Handles available!')
        print("==============================================")
        print("===================Self Configuration===================")
        print("Left Motor Handle:",leftMotorHandle)
        print("Left Wheel (front) Handle:",leftWheelFrontHandle)
        print("Left Wheel (Behind):",leftWheelBehindHandle)
        print("Left Motor Handle:",rightMotorHandle)
        print("Left Wheel (front) Handle:",rightWheelFrontHandle)
        print("Left Wheel (Behind) Handle:",rightWheelBehindHandle)
        print("===================Client Configuration===================")
        print("Left Motor Handle:",hc.leftMotorHandle)
        print("Left Wheel (front) Handle:",hc.leftWheelFrontHandle)
        print("Left Wheel (Behind):",hc.leftWheelBehindHandle)
        print("Left Motor Handle:",hc.rightMotorHandle)
        print("Left Wheel (front) Handle:",hc.rightWheelFrontHandle)
        print("Left Wheel (Behind) Handle:",hc.rightWheelBehindHandle)
        print("===============================================")

    def StopSimulation(self):
        clientID = self.clientID
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)    # Stop simulation
        vrep.simxFinish(clientID)   # Finish

# control robot by keyboard
def main():

    # variates
    resolutionX = 640               # Camera resolution: 640*480
    resolutionY = 900
    RAD2DEG = 180 / math.pi         # transform radian to degrees
    robot = robotBase()

    vec = 0.1
    
    pygame.init()
    screen = pygame.display.set_mode((resolutionX, resolutionY))
    screen.fill((255,255,255))
    pygame.display.set_caption("RobotBase Control Panel")
    # looping, can resume moving with pressing one key
    pygame.key.set_repeat(200,50)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    black = (0, 0, 0)
    manager = pygame_gui.UIManager((800, 800))
    # Introd
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 25), (160, 45)),text='Adjusting velocity',manager=manager)
    Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 25), (60, 45)),text='+0.5',manager=manager)
    Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 25), (60, 45)),text='-0.5',manager=manager)
    Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 25), (60, 45)),text='+0.1',manager=manager)
    Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 25), (60, 45)),text='-0.1',manager=manager)
    reset_button= pygame_gui.elements.UIButton(relative_rect=pygame.Rect((470, 25), (150, 45)),text='Reset Robot',manager=manager)

    # Motor left control button
    motorLeftAdd5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 75), (60, 45)),text='+0.5',manager=manager)
    motorLeftSub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 75), (60, 45)),text='-0.5',manager=manager)
    motorLeftAdd_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 75), (60, 45)),text='+0.1',manager=manager)
    motorLeftSub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 75), (60, 45)),text='-0.1',manager=manager)
    # Motor right control button
    motorRightAdd5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 125), (60, 45)),text='+0.5',manager=manager)
    motorRightSub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 125), (60, 45)),text='-0.5',manager=manager)
    motorRightAdd_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 125), (60, 45)),text='+0.1',manager=manager)
    motorRightSub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 125), (60, 45)),text='-0.1',manager=manager)
    '''
    # Motor left control button
    motorLeftAdd5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 75), (60, 45)),text='>> (R)',manager=manager)
    motorLeftSub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 75), (60, 45)),text='(Q) <<',manager=manager)
    motorLeftAdd_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 75), (60, 45)),text='> (E)',manager=manager)
    motorLeftSub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 75), (60, 45)),text='(W) <',manager=manager)
    # Motor right control button
    motorRightAdd5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 125), (60, 45)),text='>> (F)',manager=manager)
    motorRightSub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 125), (60, 45)),text='(A) <<',manager=manager)
    motorRightAdd_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 125), (60, 45)),text='> (D)',manager=manager)
    motorRightSub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 125), (60, 45)),text='(S) <',manager=manager)
    '''
    
    

    # Task 2
    massConfig_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 175), (150, 45)),text='Mass Config',manager=manager)
    setMaxTorque_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 175), (200, 45)),text='Set Motor Max Torque',manager=manager)
    setVec_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 175), (150, 45)),text='Set Velocity',manager=manager)
    
    graphCapture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 225), (150, 45)),text='Pause/Resume',manager=manager)
    scaleWheel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (150, 45)),text='Wheel Dimension',manager=manager)
    resetVec_button= pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 225), (150, 45)),text='Reset Velocity',manager=manager)

    '''
    # Version v1.0.0 (Full version)
    # Pose
    changeDirection_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 175), (150, 45)),text='Forward/Backward',manager=manager)
    setVec_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 175), (150, 45)),text='Set Velocity',manager=manager)
    resetVec_button= pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 175), (150, 45)),text='Reset Velocity',manager=manager)

    # Modify
    massIncrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 225), (150, 45)),text='Mass Increase',manager=manager)
    massDecrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (150, 45)),text='Mass Decrease',manager=manager)
    massConfig_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 225), (150, 45)),text='Mass Config',manager=manager)
    
    setMaxTorque_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((21, 275), (200, 45)),text='Set Motor Max Torque',manager=manager)
    scaleWheel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (150, 45)),text='Wheel Dimension',manager=manager)
    graphCapture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 275), (150, 45)),text='Pause/Resume',manager=manager)
    '''

    '''
    # Joint 3 button
    joint3Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 175), (45, 45)),text='>>',manager=manager)
    joint3Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 175), (45, 45)),text='<<',manager=manager)
    joint3Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 175), (45, 45)),text='> (Z)',manager=manager)
    joint3Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 175), (45, 45)),text='(X) <',manager=manager)
    # Joint 4 button
    joint4Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 225), (45, 45)),text='>>',manager=manager)
    joint4Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (45, 45)),text='<<',manager=manager)
    joint4Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 225), (45, 45)),text='> (E)',manager=manager)
    joint4Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 225), (45, 45)),text='(R) <',manager=manager)
    # Joint 5 button
    joint5Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 275), (45, 45)),text='>>',manager=manager)
    joint5Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (45, 45)),text='<<',manager=manager)
    joint5Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (45, 45)),text='> (D)',manager=manager)
    joint5Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (45, 45)),text='(F) <',manager=manager)
    # Joint 6 Button
    joint6Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 325), (45, 45)),text='>>',manager=manager)
    joint6Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 325), (45, 45)),text='<<',manager=manager)
    joint6Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 325), (45, 45)),text='> (C)',manager=manager)
    joint6Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 325), (45, 45)),text='(V) <',manager=manager)
    # Pose
    returnPose_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 375), (150, 45)),text='Home Position (L)',manager=manager)
    openRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (150, 45)),text='Open RG2 (Y)',manager=manager)
    closeRG2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 375), (150, 45)),text='Close RG2 (T)',manager=manager)
    setTarget_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((70, 425), (500, 45)),text='Joint Angle Configuration (input joint angle at administrator)',manager=manager)
    '''

    clock = pygame.time.Clock()

    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(315,845,150,32)
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('seagreen1')
    
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('white')
    color = color_passive
    
    active = False
    
    while True:
        time_delta = clock.tick(60)/1000.0
        #jointAngle = information.getJointPositionDegree()
        #targetinfo = information.getTargetInfomation()
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 20)
        X = 500
        Y = 100
        jointTitle = ['Left Motor', 'Right Motor']
        infoTitle = ['Left Motor Torque: ','Right Motor Torque: ']
        massWheelTitle = ['Robot Mass: ','Wheel Diameter: ']
        vecTitle = ["-------Linear Velocity-------","------Angular Velocity------"]
        vecInfoTitle = ["X: ","Y: ","Z: "]
        pygame.display.flip()
        
        for i in range(2):
            X = 500
            textClear = font.render('            ', True, black, white)
            if(i == 0):
                if (float(hc.leftMotorVec) >= 0 and float(hc.leftMotorVec) != -0.0):
                    text = font.render('+' + str(round(float(hc.leftMotorVec),4)), True, blue, white)
                else:
                    text = font.render(str(round(float(hc.leftMotorVec),4)), True, blue, white)
            elif(i==1):
                if (float(hc.rightMotorVec) >= 0 and float(hc.rightMotorVec) != -0.0):
                    text = font.render('+' + str(round(float(hc.rightMotorVec),4)), True, blue, white)
                else:
                    text = font.render(str(round(float(hc.rightMotorVec),4)), True, blue, white)
            textTitle = font.render(str(jointTitle[i]), True, black, white)
            textVec = font.render('rad/s', True, black, white)
            textRectClear = textClear.get_rect()
            textRect = text.get_rect()
            textRectTitle = textTitle.get_rect()
            textRectVec = textVec.get_rect()
            textRectClear.center = (X, Y + (i * 50))
            textRect.center = (X, Y + (i * 50))
            textRectTitle.center = (X-375, Y + (i * 50))
            textRectVec.center = (X+75, Y + (i * 50))
            screen.blit(textClear, textRectClear)
            screen.blit(text, textRect)
            screen.blit(textTitle, textRectTitle)
            screen.blit(textVec, textRectVec)

            #----------------------------------------Robot mass (start)----------------------------------------
            textInfoTopic = font.render('---------Robot Information---------', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 300 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 460
            textInfoTitle = font.render(str(massWheelTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            textRectInfoTitle.center = (X-355 +(i*300)  , 350)
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Mass Information Clear
            textInfoClear = font.render('                     ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            textRectInfoClear.center = (X-220 +(i*310), 350)
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Mass Information
            res, mass = info.readRobotMass()
            '''
            while res == 1:
                time.sleep(1)
                res, mass = info.readRobotMass()
            '''
            if(res == 1):
                time.sleep(1) 
                print(f"res == 1! Restart simultator")
                sys.exit("Error! Please try to launch the Task1_python.bat again!") #Terminar este script
                '''
                try:
                    vrep.simxFinish(-1) #close the previous connections
                    clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
                    print(f"Client ID is: {clientID}")
                    if clientID!=-1:
                        print ('connect successfully')
                    else:
                        sys.exit("Error: no se puede conectar") #Terminar este script
                    vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)     #Start simulation
                    print("-----------------Simulation start-----------------")
                    continue
                except:
                    print("Error at starting simultator!")
                    break
                '''
            rightTorque = info.getMotorTorque(hc.rightMotorHandle)
            #print(type(leftTorque))
            #print(type(rightTorque))
            massWheelinfo = [round(mass,4),round(hc.wheelScale,4)]
            if(i == 0):
                textInfo = font.render(str(massWheelinfo[i])+' kg', True, black, white)
            elif(i == 1):
                textInfo = font.render(str(massWheelinfo[i])+' m', True, black, white)
            textRectInfo = textInfo.get_rect()
            textRectInfo.center = (X-220 +(i*310) , 350)
            screen.blit(textInfo, textRectInfo)
            #----------------------------------------Robot mass (end)----------------------------------------

            #----------------------------------------Robot Wheel configuration (start)----------------------------------------
            #----------------------------------------Robot Wheel configuration (end)----------------------------------------


            #----------------------------------------Robot Velocity (start)----------------------------------------

            
            # Velocity Information Title
            textInfoTopic = font.render(vecTitle[i], True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 400+(i*100) )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 480
            
            
            for j in range(3):
                textInfoTitle = font.render(str(vecInfoTitle[j]), True, black, white)
                textRectInfoTitle = textInfoTitle.get_rect()
                textRectInfoTitle.center = (X-440 + (j*190) , 450+(i*100) )
                screen.blit(textInfoTitle, textRectInfoTitle)

                # Velocity Information Clear
                textInfoClear = font.render('                       ', True, black, white)
                textRectInfoClear = textInfoClear.get_rect()
                textRectInfoClear.center = (X-360+ (j*190) , 450+(i*100) )
                screen.blit(textInfoClear, textRectInfoClear)
                
                # Velocity Information
                result, linear, angular = info.getObjectVelocity(hc.robotHandle)
                #print(type(leftTorque))
                #print(type(rightTorque))
                VecX = [round(linear[0],4),round(angular[0],4)]
                VecY = [round(linear[1],4),round(angular[1],4)]
                VecZ = [round(linear[2],4),round(angular[2],4)]
                if(i==0):
                    textInfo = font.render(str(round(linear[j],4))+' m/s', True, black, white)
                if(i==1):
                    textInfo = font.render(str(round(angular[j],4))+' rad/s', True, black, white)
                textRectInfo = textInfo.get_rect()
                textRectInfo.center = (X-360+ (j*190) , 450+(i*100) )
                screen.blit(textInfo, textRectInfo)
            #----------------------------------------Robot Velocity (end)----------------------------------------


            #----------------------------------------Motor Torque (start)----------------------------------------
            # Torque Information Title
            textInfoTopic = font.render('---------Motor Torque---------', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 600 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 480
            textInfoTitle = font.render(str(infoTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            textRectInfoTitle.center = (X-355  , 650+(i*50) )
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Torque Information Clear
            textInfoClear = font.render('                     ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            textRectInfoClear.center = (X-150 , 650+(i*50) )
            screen.blit(textInfoClear, textRectInfoClear)

            textInfoClear = font.render('                                                ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            textRectInfoClear.center = (X+20 , 650+(i*50) )
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Torque Information
            leftTorque = info.getMotorTorque(hc.leftMotorHandle)
            rightTorque = info.getMotorTorque(hc.rightMotorHandle)
            leftMaxTorque = info.getMotorMaxTorque(hc.leftMotorHandle)
            rightMaxTorque = info.getMotorMaxTorque(hc.rightMotorHandle)
            #print(type(leftTorque))
            #print(type(rightTorque))
            leftTorque = round(leftTorque,4)
            rightTorque = round(rightTorque,4)
            leftMaxTorque = round(leftMaxTorque,4)
            rightMaxTorque = round(rightMaxTorque,4)

            targetinfo = [round(leftTorque,4),round(rightTorque,4)]
            maxTorqueInfo = [round(leftMaxTorque,4),round(rightMaxTorque,4)]
            
            textInfo = font.render(str(targetinfo[i])+' N m', True, black, white)
            textRectInfo = textInfo.get_rect()
            textRectInfo.center = (X-150 , 650+(i*50) )
            screen.blit(textInfo, textRectInfo)

            maxTInfo = font.render('(Max: '+str(maxTorqueInfo[i])+' Nm'+')', True, blue, white)
            maxTRectInfo = maxTInfo.get_rect()
            maxTRectInfo.center = (X+20 , 650+(i*50) )
            screen.blit(maxTInfo, maxTRectInfo)

            #----------------------------------------Motor Torque (end)----------------------------------------

            '''
            returnCode, state, forceVector, torqueVector = sensor.getForceSensor(hc.leftForceSensorHandle)
            print("----------Left Force Sensor result----------")
            print(f"Return Code is {returnCode}")
            print(f"Force Sensor State is {state}")
            print(f"Force Vector is {forceVector}")
            print(f"Torque Vector is {torqueVector}")

            returnCode, state, forceVector, torqueVector = sensor.getForceSensor(hc.rightForceSensorHandle)
            print("----------Right Force Sensor result----------")
            print(f"Return Code is {returnCode}")
            print(f"Force Sensor State is {state}")
            print(f"Force Vector is {forceVector}")
            print(f"Torque Vector is {torqueVector}")
            '''
            



            

        pygame.display.update()
        pygame.display.flip()

        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # exit the program
            if event.type == pygame.QUIT:
                reset.run()
                reset.resetJointMaxTorque(1)
                loading.scaleLoading()
                loading.placeLoading()
                is_running = False
                robot.StopSimulation()
                sys.exit()
            # click button

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == reset_button:
                        reset.run()
                        reset.resetGraph()
                        reset.resetJointMaxTorque(1)
                        loading.scaleLoading()
                        loading.placeLoading()
                        for i in range(len(hc.functionStatus)):
                            hc.functionStatus[i] = 0


                # Motor Left control
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftAdd5_button:
                        print('Motor Left Velocity increase 0.5 rad/s!')
                        velocity.motorVelocityPositive(hc.leftMotorHandle,0.5)
                        print("Left Motor Current Velocity: ",hc.leftMotorVec)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftSub5_button:
                        print('Motor Left Velocity decrease 0.5 rad/s!')
                        velocity.motorVelocityNegative(hc.leftMotorHandle,0.5)
                        print("Left Motor Current Velocity: ",hc.leftMotorVec)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftAdd_button:
                        print('Motor Left Velocity increase 0.1 rad/s!')
                        velocity.motorVelocityPositive(hc.leftMotorHandle,0.1)
                        print("Left Motor Current Velocity: ",hc.leftMotorVec)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftSub_button:
                        print('Motor Left Velocity decrease 0.1 rad/s!')
                        velocity.motorVelocityNegative(hc.leftMotorHandle,0.1)
                        print("Left Motor Current Velocity: ",hc.leftMotorVec)
                
                # Motor Right
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightAdd5_button:
                        print('Motor Right Velocity increase 0.5 rad/s!')
                        velocity.motorVelocityPositive(hc.rightMotorHandle,0.5)
                        print("Right Motor Current Velocity: ",hc.rightMotorVec)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightSub5_button:
                        print('Motor Right Velocity decrease 0.5 rad/s!')
                        velocity.motorVelocityNegative(hc.rightMotorHandle,0.5)
                        print("Right Motor Current Velocity: ",hc.rightMotorVec)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightAdd_button:
                        print('Motor Right Velocity increase 0.1 rad/s!')
                        velocity.motorVelocityPositive(hc.rightMotorHandle,0.1)
                        print("Right Motor Current Velocity: ",hc.rightMotorVec)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightSub_button:
                        print('Motor Right Velocity decrease 0.1 rad/s!')
                        velocity.motorVelocityNegative(hc.rightMotorHandle,0.1)
                        print("Right Motor Current Velocity: ",hc.rightMotorVec)
                
                # Pose

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == resetVec_button:
                        velocity.reset()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setVec_button:
                        active = True
                        #velocity.setmotorVelocity()
                        hc.functionStatus[0] = 1
                        hc.question = "Please input the angular velocity for both motor (rad/s): "
                        hc.inputHeading = 'Input: '

                # Modify

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == massConfig_button:
                        active = True
                        #modify.setRobotMass()
                        #loading.scaleLoading()
                        #loading.placeLoading()
                        hc.functionStatus[1] = 1
                        hc.question = "Please input the robot mass [10kg - 400kg] (kg): "
                        hc.inputHeading = 'Input: '
                
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setMaxTorque_button:
                        active = True
                        #modify.updateJointMaxTorque() 
                        hc.functionStatus[2] = 1
                        hc.question = "Please input the max torque of two motors (Nm): "
                        hc.inputHeading = 'Input: '
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == scaleWheel_button:
                        active = True
                        #modify.scaleWheel()
                        hc.functionStatus[3] = 1
                        hc.question = "Please input the diameter of Wheels [0.12m - 0.36m] (m): "
                        hc.inputHeading = 'Input: '
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == graphCapture_button:
                        reset.pauseOrResume()
                        


            manager.process_events(event)
            # Key used:
            # q, w, e, r, t, y, u, i, o
            # a, s, d, f, 
            # m,
            # up, down, 
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                '''
                if(event.unicode == "\b"):
                    print("K_BACKSPACE")
                elif(event.unicode == "\r"):
                    print("K_RETURN")
                print(event.unicode)
                '''
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string
                # formation
                if event.key == pygame.K_RETURN:
                    # get and print the user inputed message.
                    print("The user input: ", user_text[:])
                    hc.userInput = user_text[:]
                    print("The value passed to the function")
                    for i in range(len(hc.functionStatus)):
                        if(hc.functionStatus[i] == 1):
                            if(i == 0):
                                velocity.setmotorVelocity()
                            elif(i == 1):
                                modify.setRobotMass()
                                loading.scaleLoading()
                                loading.placeLoading()
                            elif(i == 2):
                                modify.updateJointMaxTorque()
                            elif(i == 3):
                                modify.scaleWheel()
                            # Reset the user input after function executed
                            print("i is: ",i)
                            hc.functionStatus[i] = 0
                            print(hc.functionStatus)
                            user_text = ""
                            hc.userInput = user_text
                            active = False
                            print("Status: ",hc.functionStatus)
                            #hc.question = "-------------------------------------------------------------------------------------"
                            hc.question = "                                                                                                          "
                            hc.inputHeading = "                         "
                else:
                    if(active == True):
                        if(event.unicode != "\b" and event.unicode != "\r"):
                            user_text += event.unicode
                '''
                if event.key == pygame.K_p:
                    reset.run()
                    robot.StopSimulation()
                    sys.exit()
                # Left Motor control with clicking buttons
                elif event.key == pygame.K_q:
                    velocity.motorVelocityNegative(hc.leftMotorHandle,0.5)
                elif event.key == pygame.K_w:
                    velocity.motorVelocityNegative(hc.leftMotorHandle,0.1)
                elif event.key == pygame.K_e:
                    velocity.motorVelocityPositive(hc.leftMotorHandle,0.1)
                elif event.key == pygame.K_r:
                    velocity.motorVelocityPositive(hc.leftMotorHandle,0.5)

                # Right Motor control with clicking buttons
                elif event.key == pygame.K_a:
                    velocity.motorVelocityNegative(hc.rightMotorHandle,0.5)
                elif event.key == pygame.K_s:
                    velocity.motorVelocityNegative(hc.rightMotorHandle,0.1)
                elif event.key == pygame.K_d:
                    velocity.motorVelocityPositive(hc.rightMotorHandle,0.1)
                elif event.key == pygame.K_f:
                    velocity.motorVelocityPositive(hc.rightMotorHandle,0.5)
                
                # pose
                elif event.key == pygame.K_t:
                    velocity.changeDirection()
                elif event.key == pygame.K_y:
                    velocity.reset()
                elif event.key == pygame.K_u:
                    reset.run()
                    reset.resetGraph()
                elif event.key == pygame.K_i:
                    modify.updateJointMaxTorque()
                elif event.key == pygame.K_o:
                    modify.setRobotMass()

                # modify
                elif event.key == pygame.K_UP:
                    modify.updateRobotMass(hc.robotHandle,10)
                    loading.scaleLoading()
                    loading.placeLoading()
                elif event.key == pygame.K_DOWN:
                    modify.updateRobotMass(hc.robotHandle,-10)
                    loading.scaleLoading()
                    loading.placeLoading()
                elif event.key == pygame.K_m:
                    modify.scaleWheel()
                else:
                    print("Invalid input, no corresponding function for this key!")
                '''
        questionTopicInfo = base_font.render("------------------- User Input -------------------", True, blue, white)
        questionTopic = pygame.Rect(115,750,700,32)
        screen.blit(questionTopicInfo, questionTopic)

        questionTopicInfo = base_font.render(hc.question, True, black, white)
        questionTopic = pygame.Rect(25,800,700,32)
        screen.blit(questionTopicInfo, questionTopic)

        inputTopicInfo = base_font.render(hc.inputHeading, True, blue, white)
        inputTopic = pygame.Rect(240,850,50,32)
        screen.blit(inputTopicInfo, inputTopic)

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
  
        text_surface = base_font.render(user_text, True, (0,0,0))
        
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)

        clock.tick(60)

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
                    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
        reset.run()
        sys.exit(0)

