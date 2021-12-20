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

    def openRG2(self):
        rgName = self.rgName
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
                                                        vrep.sim_scripttype_childscript,'rg2Open',[],[],[],b'',vrep.simx_opmode_blocking)
        
    # close rg2
    def closeRG2(self):
        rgName = self.rgName
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, rgName,\
                                                        vrep.sim_scripttype_childscript,'rg2Close',[],[],[],b'',vrep.simx_opmode_blocking)
        
    def StopSimulation(self):
        clientID = self.clientID
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)    # Stop simulation
        vrep.simxFinish(clientID)   # Finish
    

    


# control robot by keyboard
def main():
    # variates
    resolutionX = 640               # Camera resolution: 640*480
    resolutionY = 680
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
    manager = pygame_gui.UIManager((800, 600))
    # Introd
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 25), (160, 45)),text='Adjusting velocity',manager=manager)
    Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 25), (60, 45)),text='+0.5',manager=manager)
    Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 25), (60, 45)),text='-0.5',manager=manager)
    Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 25), (60, 45)),text='+0.1',manager=manager)
    Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 25), (60, 45)),text='-0.1',manager=manager)
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
    
    # Pose
    changeDirection_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 175), (150, 45)),text='Forward/Backward',manager=manager)
    reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 175), (150, 45)),text='Reset Velocity',manager=manager)
    reset_button= pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 175), (150, 45)),text='Reset Robot',manager=manager)

    # Modify
    massIncrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 225), (150, 45)),text='Mass Increase',manager=manager)
    massDecrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (150, 45)),text='Mass Decrease',manager=manager)
    scaleWheel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 225), (150, 45)),text='Wheel Dimension',manager=manager)
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
        vecTitle = ["---Linear Velocity---","---Angular Velocity---"]
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

            #----------------------------------------Robot Velocity (start)----------------------------------------

            
            # Velocity Information Title
            textInfoTopic = font.render('---------Robot Velocity---------', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 300 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            textInfoTopic = font.render(vecTitle[i], True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 350+(i*100) )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 480
            
            
            for j in range(3):
                textInfoTitle = font.render(str(vecInfoTitle[j]), True, black, white)
                textRectInfoTitle = textInfoTitle.get_rect()
                textRectInfoTitle.center = (X-440 + (j*190) , 400+(i*100) )
                screen.blit(textInfoTitle, textRectInfoTitle)

                # Velocity Information Clear
                textInfoClear = font.render('                       ', True, black, white)
                textRectInfoClear = textInfoClear.get_rect()
                textRectInfoClear.center = (X-360+ (j*190) , 400+(i*100) )
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
                textRectInfo.center = (X-360+ (j*190) , 400+(i*100) )
                screen.blit(textInfo, textRectInfo)
            #----------------------------------------Robot Velocity (end)----------------------------------------


            #----------------------------------------Motor Torque (start)----------------------------------------
            # Torque Information Title
            textInfoTopic = font.render('---------Motor Torque---------', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 550 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 480
            textInfoTitle = font.render(str(infoTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            textRectInfoTitle.center = (X-355  , 600+(i*50) )
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Torque Information Clear
            textInfoClear = font.render('                     ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            textRectInfoClear.center = (X-150 , 600+(i*50) )
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Torque Information
            leftTorque = info.getMotorTorque(hc.leftMotorHandle)
            rightTorque = info.getMotorTorque(hc.rightMotorHandle)
            #print(type(leftTorque))
            #print(type(rightTorque))
            leftTorque = round(leftTorque,4)
            rightTorque = round(rightTorque,4)
            targetinfo = [round(leftTorque,4),round(rightTorque,4)]
            textInfo = font.render(str(targetinfo[i])+' N m', True, black, white)
            textRectInfo = textInfo.get_rect()
            textRectInfo.center = (X-150 , 600+(i*50) )
            screen.blit(textInfo, textRectInfo)

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
                is_running = False
                sys.exit()
            # click button
            if event.type == pygame.USEREVENT:
                # Motor Left control
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftAdd5_button:
                        print('Motor Left Velocity increase 0.5 m/s!')
                        print("Left Motor Current Veclocity: ",hc.leftMotorVec)
                        velocity.motorVeclocityPositive(hc.leftMotorHandle,0.5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftSub5_button:
                        print('Motor Left Velocity decrease 0.5 m/s!')
                        print("Left Motor Current Veclocity: ",hc.leftMotorVec)
                        velocity.motorVeclocityNegative(hc.leftMotorHandle,0.5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftAdd_button:
                        print('Motor Left Velocity increase 0.1 m/s!')
                        print("Left Motor Current Veclocity: ",hc.leftMotorVec)
                        velocity.motorVeclocityPositive(hc.leftMotorHandle,0.1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorLeftSub_button:
                        print('Motor Left Velocity decrease 0.1 m/s!')
                        print("Left Motor Current Veclocity: ",hc.leftMotorVec)
                        velocity.motorVeclocityNegative(hc.leftMotorHandle,0.1)
                
                # Motor Right
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightAdd5_button:
                        print('Motor Right Velocity increase 0.5 m/s!')
                        print("Right Motor Current Veclocity: ",hc.rightMotorVec)
                        velocity.motorVeclocityPositive(hc.rightMotorHandle,0.5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightSub5_button:
                        print('Motor Right Velocity decrease 0.5 m/s!')
                        print("Right Motor Current Veclocity: ",hc.rightMotorVec)
                        velocity.motorVeclocityNegative(hc.rightMotorHandle,0.5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightAdd_button:
                        print('Motor Right Velocity increase 0.1 m/s!')
                        print("Right Motor Current Veclocity: ",hc.rightMotorVec)
                        velocity.motorVeclocityPositive(hc.rightMotorHandle,0.1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == motorRightSub_button:
                        print('Motor Right Velocity decrease 0.1 m/s!')
                        print("Right Motor Current Veclocity: ",hc.rightMotorVec)
                        velocity.motorVeclocityNegative(hc.rightMotorHandle,0.1)
                
                # Pose
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == changeDirection_button:
                        velocity.changeDirection()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == reset_button:
                        velocity.reset()

                # Modify
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == massIncrease_button:
                        modify.updateRobotMass(hc.robotHandle,10)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == massDecrease_button:
                        modify.updateRobotMass(hc.robotHandle,-10)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == scaleWheel_button:
                        modify.scaleWheel()
                
                '''
                # Joint 3
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Add5_button:
                        print('Joint 3 Add 5!')
                        movement.rotateCertainAnglePositive(2,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Sub5_button:
                        print('Joint 3 Sub 5!')
                        movement.rotateCertainAngleNegative(2,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Add_button:
                        print('Joint 3 Add!')
                        movement.rotateCertainAnglePositive(2,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint3Sub_button:
                        print('Joint 3 Sub!')
                        movement.rotateCertainAngleNegative(2,1)
                # Joint 4
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Add5_button:
                        print('Joint 4 Add 5!')
                        movement.rotateCertainAnglePositive(3,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Sub5_button:
                        print('Joint 4 Sub 5!')
                        movement.rotateCertainAngleNegative(3,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Add_button:
                        print('Joint 4 Add!')
                        movement.rotateCertainAnglePositive(3,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint4Sub_button:
                        print('Joint 4 Sub!')
                        movement.rotateCertainAngleNegative(3,1)
                # Joint 5
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Add5_button:
                        print('Joint 5 Add 5!')
                        movement.rotateCertainAnglePositive(4,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Sub5_button:
                        print('Joint 5 Sub 5!')
                        movement.rotateCertainAngleNegative(4,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Add_button:
                        print('Joint 5 Add!')
                        movement.rotateCertainAnglePositive(4,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint5Sub_button:
                        print('Joint 5 Sub!')
                        movement.rotateCertainAngleNegative(4,1)
                # Joint 6
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Add5_button:
                        print('Joint 6 Add 5!')
                        movement.rotateCertainAnglePositive(5,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Sub5_button:
                        print('Joint 6 Sub 5!')
                        movement.rotateCertainAngleNegative(5,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Add_button:
                        print('Joint 6 Add!')
                        movement.rotateCertainAnglePositive(5,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint6Sub_button:
                        print('Joint 6 Sub!')
                        movement.rotateCertainAngleNegative(5,1)
                # Pose
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == returnPose_button:
                        robot.returnPose()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == openRG2_button:
                        robot.openRG2()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == closeRG2_button:
                        robot.closeRG2()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == setTarget_button:
                        robot.setJointAngle()               
                '''
            manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    robot.StopSimulation()
                    sys.exit()
                # Left Motor control with clicking buttons
                elif event.key == pygame.K_q:
                    velocity.motorVeclocityNegative(hc.leftMotorHandle,0.5)
                elif event.key == pygame.K_w:
                    velocity.motorVeclocityNegative(hc.leftMotorHandle,0.1)
                elif event.key == pygame.K_e:
                    velocity.motorVeclocityPositive(hc.leftMotorHandle,0.1)
                elif event.key == pygame.K_r:
                    velocity.motorVeclocityPositive(hc.leftMotorHandle,0.5)

                # Right Motor control with clicking buttons
                elif event.key == pygame.K_a:
                    velocity.motorVeclocityNegative(hc.rightMotorHandle,0.5)
                elif event.key == pygame.K_s:
                    velocity.motorVeclocityNegative(hc.rightMotorHandle,0.1)
                elif event.key == pygame.K_d:
                    velocity.motorVeclocityPositive(hc.rightMotorHandle,0.1)
                elif event.key == pygame.K_f:
                    velocity.motorVeclocityPositive(hc.rightMotorHandle,0.5)
                
                # pose
                elif event.key == pygame.K_t:
                    velocity.changeDirection()
                elif event.key == pygame.K_y:
                    velocity.reset()

                # modify
                elif event.key == pygame.K_UP:
                    modify.updateRobotMass(hc.robotHandle,10)
                elif event.key == pygame.K_DOWN:
                    modify.updateRobotMass(hc.robotHandle,-10)
                elif event.key == pygame.m:
                    modify.scaleWheel()
                else:
                    print("Invalid input, no corresponding function for this key!")


        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
                    
if __name__ == '__main__':
    main()
