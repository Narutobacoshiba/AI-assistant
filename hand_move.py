
import cv2
import numpy as np
import math,time
from keyboard import Keyboard

def catch_hand_move():
    p = Keyboard()
    cap = cv2.VideoCapture(0)
    i = 0
    up = 0
    down = 0
    left = 0
    right = 0

    for i in range(0,30):
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)
            
        roi=frame[100:400, 400:650]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
            

        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        up_n = cv2.countNonZero(mask[0:150,120:240])
        if up_n > up:
            up = up_n
        down_n = cv2.countNonZero(mask[150:300,120:240])
        if down_n > down:
            down = down_n
        left_n = cv2.countNonZero(mask[50:250,0:120])
        if left_n > left:
            left = left_n
        right_n = cv2.countNonZero(mask[50:250,240:360])
        if right_n > right:
            right = right_n

    is_up = 0
    is_down = 0
    is_left = 0
    is_right = 0

    while True:
        
        try:  #an error comes if it does not find anything in window as it cannot find contour of max area
            #therefore this try error statement
            
            ret, frame = cap.read()
            frame=cv2.flip(frame,1)
            kernel = np.ones((3,3),np.uint8)
            
            #define region of interest
            roi=frame[100:400, 300:660]
            frame=frame[100:400, 300:660]
            
            cv2.rectangle(frame,(120,0),(240,150),(0,255,0),0) 
            cv2.rectangle(frame,(0,50),(120,250),(0,255,0),0)
            cv2.rectangle(frame,(120,150),(240,300),(0,255,0),0)
            cv2.rectangle(frame,(240,50),(360,250),(0,255,0),0)   
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            
            
        # define range of skin color in HSV
            lower_skin = np.array([0,20,70], dtype=np.uint8)
            upper_skin = np.array([20,255,255], dtype=np.uint8)
            
        #extract skin colur imagw  
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
    
            
        #extrapolate the hand to fill dark spots within
            #mask = cv2.dilate(mask,kernel,iterations = 4)
            
        #blur the image
            #mask = cv2.GaussianBlur(mask,(5,5),100)
            
            

            
            up_c = cv2.countNonZero(mask[0:150,120:240]) - up
            down_c = cv2.countNonZero(mask[150:300,120:240]) - down

            left_c = cv2.countNonZero(mask[50:250,0:120]) - left
            right_c = cv2.countNonZero(mask[50:250,240:360]) - right
            
            if up_c + down_c + left_c + right_c < 7000:
                is_up = 0
                is_down = 0
                is_left = 0
                is_right = 0
            else:
                maxs = max([up_c,left_c,right_c,down_c])
                if up_c == maxs:
                    is_up += 1
                    is_down = 0
                    is_left = 0
                    is_right = 0
                    if is_up == 5:
                        p.key(p.VK_UP,0.01)
                        p.key(p.VK_UP,0.01)
                        is_up = 0
                elif down_c == maxs:
                    is_down += 1
                    is_up = 0
                    is_left = 0
                    is_right = 0
                    if is_down == 5:
                        p.key(p.VK_DOWN,0.01)
                        p.key(p.VK_DOWN,0.01)  
                        is_down = 0
                elif left_c == maxs:
                    is_left += 1
                    is_up = 0
                    is_down = 0
                    is_right = 0
                    if is_left == 20:
                        p.key(p.VK_LEFT,0.01)
                        is_left = 0
                elif right_c == maxs:
                    is_right += 1
                    is_up = 0
                    is_down = 0
                    is_left = 0
                    if is_right == 20:
                        p.key(p.VK_RIGHT,0.01) 
                        is_right = 0

                
            
            
            

            
        #find contours
            """
            contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
    #find contour of max area(hand)
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
            
        #approx the contour a little
            epsilon = 0.0005*cv2.arcLength(cnt,True)
            approx= cv2.approxPolyDP(cnt,epsilon,True)
            
            
            
        #make convex hull around hand
            hull = cv2.convexHull(cnt)
            
        #define area of hull and area of hand
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)
        
        #find the percentage of area not covered by hand in convex hull
            arearatio=((areahull-areacnt)/areacnt)*100
            
        #find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)
            
        # l = no. of defects
        
            l=0
            
        #code for finding no. of defects due to fingers
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt= (100,180)
                
                
                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                
                #distance between point and convex hull
                d=(2*ar)/a
                
                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                
            
                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d>30:
                    l += 1
                    cv2.circle(roi, far, 3, [255,0,0], -1)
                
                #draw lines around hand
                cv2.line(roi,start, end, [0,255,0], 2)
                
            
            l+=1
            
            #print corresponding gestures which are in their ranges
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            if l==1:
                if areacnt<2000:
                    cv2.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                else:
                    if arearatio<12:
                        cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    elif arearatio<17.5:
                        cv2.putText(frame,'Best of luck',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                    else:
                        cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                        
            elif l==2:
                cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                
            elif l==3:
            
                if arearatio<27:
                        cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                else:
                        cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                        
            elif l==4:
                cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                
            elif l==5:
                cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                
            elif l==6:
                cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                
            else :
                cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            """
            #show the windows
            cv2.imshow('mask',mask)
            cv2.imshow('frame',frame)

        except:
            pass
            
        
        k = cv2.waitKey(5) & 0xff
        
        if k == 27:
            break
        
    cv2.destroyAllWindows()
    cap.release()

catch_hand_move()