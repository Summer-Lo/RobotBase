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
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 25), (185, 45)),text='Adjusting Joint Angle',manager=manager)
    Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 25), (45, 45)),text='+5',manager=manager)
    Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 25), (45, 45)),text='-5',manager=manager)
    Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 25), (45, 45)),text='+1',manager=manager)
    Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 25), (45, 45)),text='-1',manager=manager)
    # Joint 1 button
    joint1Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 75), (45, 45)),text='>>',manager=manager)
    joint1Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 75), (45, 45)),text='<<',manager=manager)
    joint1Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 75), (45, 45)),text='> (Q)',manager=manager)
    joint1Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 75), (45, 45)),text='(W) <',manager=manager)
    # Joint 2 button
    joint2Add5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 125), (45, 45)),text='>>',manager=manager)
    joint2Sub5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 125), (45, 45)),text='<<',manager=manager)
    joint2Add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 125), (45, 45)),text='> (A)',manager=manager)
    joint2Sub_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 125), (45, 45)),text='(S) <',manager=manager)
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
    
    clock = pygame.time.Clock()
    # Configurating RG2
    robot.closeRG2()

    time.sleep(1)

    robot.openRG2()

    time.sleep(1)

    robot.closeRG2()

    time.sleep(1)

    robot.openRG2()
    
    while True:
        time_delta = clock.tick(60)/1000.0
        jointAngle = [0,0,0,0,0,0]
        jointAngle = information.getJointPositionDegree()
        targetinfo = information.getTargetInfomation()
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 20)
        X = 500
        Y = 100
        jointTitle = ['Base (Joint1)','Shoulder (Joint2)','Elbow (Joint3)','Wrist 1 (Joint4)','Wrist 2 (Joint5)','Wrist 3 (Joint6)']
        infoTitle = ['X:','Y:','Z:','Alpha: ','Beta: ','Gamma: ']
        pygame.display.flip()
        for i in range(6):
            X = 500
            textClear = font.render('              ', True, black, white)
            if (jointAngle[i] >= 0 and jointAngle[i] != -0.0):
                text = font.render('+' + str(jointAngle[i]), True, blue, white)
            else:
                text = font.render(str(jointAngle[i]), True, blue, white)
            textTitle = font.render(str(jointTitle[i]), True, black, white)
            textDegree = font.render('deg', True, black, white)
            textRectClear = textClear.get_rect()
            textRect = text.get_rect()
            textRectTitle = textTitle.get_rect()
            textRectDegree = textDegree.get_rect()
            textRectClear.center = (X, Y + (i * 50))
            textRect.center = (X, Y + (i * 50))
            textRectTitle.center = (X-375, Y + (i * 50))
            textRectDegree.center = (X+75, Y + (i * 50))
            screen.blit(textClear, textRectClear)
            screen.blit(text, textRect)
            screen.blit(textTitle, textRectTitle)
            screen.blit(textDegree, textRectDegree)
            # Target Information Title
            textInfoTopic = font.render('---End-Effector (Tip) Position and Orientation---', True, blue, white)
            textRectInfoTopic = textInfoTopic.get_rect()
            textRectInfoTopic.center = (310, 500 )
            screen.blit(textInfoTopic, textRectInfoTopic)
            X = 480
            textInfoTitle = font.render(str(infoTitle[i]), True, black, white)
            textRectInfoTitle = textInfoTitle.get_rect()
            if (i <= 2):
                textRectInfoTitle.center = (X-400 +(i*200), 550 )
            else:
                textRectInfoTitle.center = (X-400 +((i-3)*187), 600 )
            screen.blit(textInfoTitle, textRectInfoTitle)
            
            # Target Information Clear
            textInfoClear = font.render('                 ', True, black, white)
            textRectInfoClear = textInfoClear.get_rect()
            if (i <= 2):
                textRectInfoClear.center = (X-330 +(i*200), 550 )
            elif (i == 3):
                textRectInfoClear.center = (X-320, 600 )
            elif (i == 4):
                textRectInfoClear.center = (X-140, 600 )
            elif (i == 5):
                textRectInfoClear.center = (X+75, 600 )
            screen.blit(textInfoClear, textRectInfoClear)
            
            # Target Information
            if (i <= 2):
                textInfo = font.render(str(targetinfo[i])+' m', True, black, white)
            else:
                textInfo = font.render(str(targetinfo[i]), True, black, white)
            textRectInfo = textInfo.get_rect()
            if (i <= 2):
                textRectInfo.center = (X-330 +(i*200), 550 )
            elif (i == 3):
                textRectInfo.center = (X-320, 600 )
            elif (i == 4):
                textRectInfo.center = (X-140, 600 )
            elif (i == 5):
                textRectInfo.center = (X+75, 600 )
            screen.blit(textInfo, textRectInfo)
            
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
                # Joint 1
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Add5_button:
                        print('Joint 1 Add 5!')
                        movement.rotateCertainAnglePositive(0,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Sub5_button:
                        print('Joint 1 Sub 5!')
                        movement.rotateCertainAngleNegative(0,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Add_button:
                        print('Joint 1 Add!')
                        movement.rotateCertainAnglePositive(0,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint1Sub_button:
                        print('Joint 1 Sub!')
                        movement.rotateCertainAngleNegative(0,1)
                # Joint 2
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Add5_button:
                        print('Joint 2 Add 5!')
                        movement.rotateCertainAnglePositive(1,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Sub5_button:
                        print('Joint 2 Sub 5!')
                        movement.rotateCertainAngleNegative(1,5)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Add_button:
                        print('Joint 2 Add!')
                        movement.rotateCertainAnglePositive(1,1)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == joint2Sub_button:
                        print('Joint 2 Sub!')
                        movement.rotateCertainAngleNegative(1,1)
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

            manager.process_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    robot.StopSimulation()
                    sys.exit()
                # joinit 0
                elif event.key == pygame.K_q:
                    movement.rotateCertainAnglePositive(0, angle)
                elif event.key == pygame.K_w:
                    movement.rotateCertainAngleNegative(0, angle)
                # joinit 1
                elif event.key == pygame.K_a:
                    movement.rotateCertainAnglePositive(1, angle)
                elif event.key == pygame.K_s:
                    movement.rotateCertainAngleNegative(1, angle)
                # joinit 2
                elif event.key == pygame.K_z:
                    movement.rotateCertainAnglePositive(2, angle)
                elif event.key == pygame.K_x:
                    movement.rotateCertainAngleNegative(2, angle)
                # joinit 3
                elif event.key == pygame.K_e:
                    movement.rotateCertainAnglePositive(3, angle)
                elif event.key == pygame.K_r:
                    movement.rotateCertainAngleNegative(3, angle)
                # joinit 4
                elif event.key == pygame.K_d:
                    movement.rotateCertainAnglePositive(4, angle)
                elif event.key == pygame.K_f:
                    movement.rotateCertainAngleNegative(4, angle)
                # joinit 5
                elif event.key == pygame.K_c:
                    movement.rotateCertainAnglePositive(5, angle)
                elif event.key == pygame.K_v:
                    movement.rotateCertainAngleNegative(5, angle)
                # close RG2
                elif event.key == pygame.K_t:
                    robot.closeRG2()
                # # open RG2
                elif event.key == pygame.K_y:
                    robot.openRG2()
                else:
                    print("Invalid input, no corresponding function for this key!")


        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
                    
if __name__ == '__main__':
    main()
