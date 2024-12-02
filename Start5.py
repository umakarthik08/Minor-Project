from MainWindow import Ui_Visionary
import sys
import os
import cv2
import math
import cv2 as cv
import mediapipe as mp
import os
import numpy as np
import pyautogui
import time
from PySide6 import QtWidgets
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QSize, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtUiTools import QUiLoader
import subprocess

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
leftEye = [362, 382, 381, 381, 374, 373, 390,
    249, 263, 466, 388, 387, 386, 385, 384, 398]
left_iris = [474, 475, 476, 477]
right_iris = [469, 470, 471, 472]
rightEye = [33, 7, 163, 144, 145, 153, 154,
    155, 133, 173, 157, 158, 159, 160, 161, 246]
LHLeft = [33]
LHRight = [133]
RHLeft = [362]
RHRight = [263]
scale = 25
font = cv2.FONT_HERSHEY_SIMPLEX
org = (200, 50)
org1 = (130, 50)
fontScale = 1
color = (0, 0, 0)
thickness = 2

class MainWindow(QtWidgets.QMainWindow, Ui_Visionary):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.video_size = QSize(420, 340)
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.Start.pressed.connect(self.start_camera)
        self.Stop.pressed.connect(self.stop_camera)
        self.EnableScroll.pressed.connect(self.scroll_activate)
        self.DisableScroll.pressed.connect(self.scroll_deactivate)
        self.EnableOSK.pressed.connect(self.osk_activate)
        self.osk_opened = False
        # self.DisableOSK.pressed.connect(self.osk_deactivate)
        self.f = False
        self.cnt = 0
        self.scroll = 0
        self.double_blink_count = 0  # Counter for consecutive blinks scroll
        self.double_blink_count_osk = 0  # Counter for consecutive blinks osk
        self.last_blink_time = 0     # Timestamp for last blink scroll
        self.last_blink_time_osk = 0     # Timestamp for last blink osk
        
        self.leftEyeCalibration, self.rightEyeCalibration = [], []
        self.leftEyeClosed, self.rightEyeClosed = 0, 0
        self.leftEyedownCalibration, self.rightEyedownCalibration = [], []
        self.leftEyedownMax, self.rightEyedownMax =0, 0
        self.leftEyedownMin, self.rightEyedownMin =0, 0
        self.cntBlink = 0
        my_pixmap = QPixmap("./logo.png")
        my_icon = QIcon(my_pixmap)
        self.setWindowIcon(my_icon)
        #for default starting camera use below line of code by removing comment
        #self.start_camera() 

    def stop_camera(self):
        self.TEXT.setText('Kindly Press Start to open the Webcam')
        self.cntBlink = 0
        self.f = False

    def scroll_activate(self):
        self.scroll = 1
        print("Hello")
    
    def scroll_deactivate(self):
        self.scroll = 0
    
    def osk_activate(self):
        if not self.osk_opened:
            self.osk_process = subprocess.Popen("osk", shell=True)
            self.osk_opened = True

    def osk_deactivate(self):
        if self.osk_opened:
            self.osk_process.terminate()
            self.osk_opened = False


    def start_camera(self):
        """Initialize camera.
        """
        self.cnt = 0
        self.f = True
        self.TEXT.setText('Kindly Press Stop to close the Webcam')
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(0)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        if self.f:
            self.image_label.setHidden(False)
            _, frame = self.capture.read()
            frame = cv.flip(frame, 1)
            height, width, channels = frame.shape

            centerX, centerY = int(height/2), int(width/2)
            radiusX, radiusY = int(scale*height/100), int(scale*width/100)

            minX, maxX = centerX-radiusX, centerX+radiusX
            minY, maxY = centerY-radiusY, centerY+radiusY

            cropped = frame[minX:maxX, minY:maxY]
            frame = cv.resize(cropped, (width, height))
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w = frame.shape[:2]
            if landmark_points:
                landmarks = landmark_points[0].landmark

                xc1, yc1 = landmarks[475].x * \
                    frame_w, landmarks[475].y * frame_h
                xc2, yc2 = landmarks[477].x * \
                    frame_w, landmarks[477].y * frame_h
                # print(xc1+xc2)
                xc, yc = (xc1+xc2)/2, (yc1+yc2)/2
                xl, yl = landmarks[362].x * frame_w, landmarks[362].y * frame_h
                xr, yr = landmarks[263].x * frame_w, landmarks[263].y * frame_h
                xret, yret = landmarks[386].x * \
                    frame_w, landmarks[386].y * frame_h
                xreb, yreb = landmarks[374].x * \
                    frame_w, landmarks[374].y * frame_h
                xlet, ylet = landmarks[159].x * \
                    frame_w, landmarks[159].y * frame_h
                xleb, yleb = landmarks[145].x * \
                    frame_w, landmarks[145].y * frame_h
                landmark = landmarks[1]
                """if f:
                    xinit, yinit = int(
                        landmark.x * frame_w), int(landmark.y * frame_h)
                    f=0
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                if y - yinit > 25:
                    pyautogui.move(0, 30)
                elif yinit - y > 20:
                    pyautogui.move(0, -30)"""

                # 477 159
                left = [landmarks[145], landmarks[159]]
                right = [landmarks[374], landmarks[386]]
                p1, p2 = landmarks[477], landmarks[374]

                # print(p1.y * frame_h - p2.y * frame_h)

                # print(left[0].y - left[1].y, 'left')

                if self.cnt <= 100:
                    frame = cv2.putText(frame, 'Close left eye', org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
                    self.cnt += 1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))

                elif self.cnt <= 200:
                    a = 1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))
                    self.leftEyeCalibration.append(left[0].y-left[1].y)
                    #self.leftEyeClosed = (max(self.leftEyeCalibration)+min(self.leftEyeCalibration))/2
                    self.leftEyeClosed = max(self.leftEyeCalibration)
                    print("value_left:", self.leftEyeClosed)
                  

                    if a == 1:
                        frame = cv2.putText(frame, 'Close left eye : CALIBRATING', org1, font,
                       fontScale, color, thickness, cv2.LINE_AA)
                    else:
                        frame = cv2.putText(frame, 'Close left eye', org1, font,
                       fontScale, color, thickness, cv2.LINE_AA)
                    if self.cnt % 20 == 0: a = 1-a
                    self.cnt += 1

                elif self.cnt <= 300:
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0,255,0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0,255,0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0,255,0))
                    frame = cv2.putText(frame, 'Close right eye', org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
                    self.cnt+=1
                
                elif self.cnt<=400:
                    a=1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0,255,0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0,255,0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0,255,0))
                    self.rightEyeCalibration.append(right[0].y-right[1].y)
                    #self.rightEyeClosed = (max(self.rightEyeCalibration)+min(self.rightEyeCalibration))/2
                    self.rightEyeClosed = max(self.rightEyeCalibration)
                    print("value_right:", self.rightEyeClosed)


                    if a==1:
                        frame = cv2.putText(frame, 'Close right eye: CALIBRATING', org1, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
                    else:
                        frame = cv2.putText(frame, 'Close right eye', org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
                    if self.cnt%20==0: a=1-a
                    self.cnt+=1
                
                elif self.cnt <= 500:
                   
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))
                    frame = cv2.putText(frame, 'relax', org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
                    self.cnt += 1

                elif self.cnt <= 800:
                   
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))
                    frame = cv2.putText(frame, 'Look down', org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
                    self.cnt += 1

                elif self.cnt <= 900:
                    a = 1
                    cv.circle(frame, (int(xret), int(yret)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xreb), int(yreb)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xlet), int(ylet)), 3, (0, 255, 0))
                    cv.circle(frame, (int(xleb), int(yleb)), 3, (0, 255, 0))
                    self.leftEyedownCalibration.append(left[0].y-left[1].y)
                    self.rightEyedownCalibration.append(right[0].y-right[1].y)
                    #self.leftEyeClosed = (max(self.leftEyeCalibration)+min(self.leftEyeCalibration))/2
                    self.leftEyedownMax= max(self.leftEyedownCalibration)
                    self.leftEyedownMin= min(self.leftEyedownCalibration)
                    self.rightEyedownMax= max(self.rightEyedownCalibration)
                    self.rightEyedownMin= min(self.rightEyedownCalibration)
                    
                  

                    if a == 1:
                        frame = cv2.putText(frame, 'Look down: CALIBRATING', org1, font,
                       fontScale, color, thickness, cv2.LINE_AA)
                    else:
                        frame = cv2.putText(frame, 'Look down', org1, font,
                       fontScale, color, thickness, cv2.LINE_AA)
                    if self.cnt % 20 == 0: a = 1-a
                    self.cnt += 1
                
                
                
                
                
                
                
                
                
                
                else:
                    
                    # cv.circle(frame, (xinit, yinit), 20, (0,255,0))
                    iris_pos = self.iris_position([xc, yc] , [xr, yr] , [xl, yl] , [xret, yret] , [xreb, yreb])
                    if p1.y * frame_h - p2.y * frame_h < -0.8:
                        iris_pos = 'up'
                        if(self.scroll == 0): 
                            pyautogui.move(0, -20)
                        elif(self.scroll):
                            pyautogui.scroll(30)
                    if iris_pos == 'right':
                        pyautogui.move(20,0)
                        #print("value_right:", self.rightEyeClosed)
                        
                    elif iris_pos == 'left':
                        pyautogui.move(-20,0)
                        #print("value_left:", self.leftEyeClosed)
                    
                    # print((left[0].y - left[1].y), self.leftEyeClosed, "left")
                    # print((right[0].y - right[1].y), self.rightEyeClosed, "right")
                 
                    if (left[0].y - left[1].y) < self.leftEyeClosed and (right[0].y - right[1].y) < self.rightEyeClosed:
                        self.cntBlink+=1
                        if self.cntBlink>5:
                            current_time = time.time()
                            if current_time - self.last_blink_time < 1:  # Consecutive blink within 1 second
                                self.double_blink_count += 1
                                if self.double_blink_count == 2:  # Double blink detected
                                    self.scroll = not self.scroll  # Toggle scroll mode
                                    self.TEXT.setText('Scrolling activated' if self.scroll else 'Scrolling deactivated')
                                    self.double_blink_count = 0  # Reset double blink counter
                            else:
                                self.double_blink_count = 1  # Reset and start new count
                            self.last_blink_time = current_time  # Update last blink t
                        
                    elif ((self.leftEyedownMin)<(left[0].y - left[1].y) < (self.leftEyedownMax)) and ((self.rightEyedownMin)<(right[0].y - right[1].y) < (self.rightEyedownMax)):
                        self.cntBlink+=1
                        if self.cntBlink>5:
                            if(self.scroll == 0): 
                                pyautogui.move(0, 10)
                            elif(self.scroll):
                                pyautogui.scroll(-30)            
                    elif (left[0].y - left[1].y) < self.leftEyeClosed:
                        self.cntBlink+=1
                        if self.cntBlink>6:
                            if(self.scroll==0):
                               pyautogui.click() 
                               
                        

                    elif (right[0].y - right[1].y) < self.rightEyeClosed:
                        self.cntBlink+=1
                        if self.cntBlink>5:
                            current_time_osk = time.time()      
                            if current_time_osk - self.last_blink_time_osk < 1:  # Consecutive blink within 1 second
                                self.double_blink_count_osk += 1
                                if self.double_blink_count_osk == 2:  # Double blink detected
                                    if not self.osk_opened:
                                        subprocess.Popen("osk", shell=True)
                                        self.osk_opened = True
                                    if self.osk_opened:
                                        subprocess.Popen("osk", shell=True).terminate()
                                        self.osk_opened = False
                                    self.double_blink_count_osk = 0
                            else:
                                self.double_blink_count_osk = 1  # Reset and start new count
                            self.last_blink_time_osk = current_time_osk  # Update last blink time
                            if(self.scroll==0):
                               pyautogui.click(button='right')
                    else:
                        self.cntBlink = 0

            image = QImage(frame, frame.shape[1], frame.shape[0], 
                            frame.strides[0], QImage.Format_BGR888)
            self.image_label.setPixmap(QPixmap.fromImage(image))   
            self.image_label.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    
            
        else:
            self.image_label.setHidden(True)
            
            
    def iris_position(self, iris_center, right_point, left_point, top_point, bottom_point):
        ctrd = self.distance(iris_center, right_point)
        totald = self.distance(right_point, left_point)

        center_bot_diff = self.distance(iris_center, bottom_point)
        top_bot_diff = self.distance(top_point, bottom_point)

        ratio1 = ctrd / totald
        ratio2 = center_bot_diff / top_bot_diff

        iris_position = ""
        # print(ratio1)
        if ratio1<=0.38:
            iris_position = "right"
        elif ratio1>0.60:
            iris_position = "left"
        else:    
            iris_position  = "center"

        return iris_position
    
    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
        return distance     


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()