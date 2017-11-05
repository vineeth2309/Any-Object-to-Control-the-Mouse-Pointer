
import cv2
import numpy as np
import time
import win32api, win32con
#import pyautogui


cap=cv2.VideoCapture(0)
def f(x):
    return x

cv2.namedWindow('trackbars')
set=0
area1=0.0
cx1=0
cy1=0

#b=0x42     #http://msdn.microsoft.com/en-us/library/windows/desktop/dd375731%28v=vs.85%29.aspx 
#shift = 0x10
#ctrl = 0x11
#win32api.keybd_event(ctrl,0,0,0)
#win32api.keybd_event(shift,0,0,0)
#win32api.keybd_event(b,0,0,0)# holds the "F" key down
#win32api.keybd_event(ctrl,0,win32con.KEYEVENTF_KEYUP,0)
#win32api.keybd_event(shift,0,win32con.KEYEVENTF_KEYUP,0)
#win32api.keybd_event(b,0,win32con.KEYEVENTF_KEYUP,0)#     releases the key
cv2.createTrackbar('Lower H','trackbars',0,255,f)
cv2.createTrackbar('Higher H','trackbars',0,255,f)
cv2.createTrackbar('Lower S','trackbars',0,255,f)
cv2.createTrackbar('Higher S','trackbars',0,255,f)
cv2.createTrackbar('Lower V','trackbars',0,255,f)
cv2.createTrackbar('Higher V','trackbars',0,255,f)

while(cap.isOpened()):
    ret,frame1=cap.read()
    frame1 = cv2.resize(frame1,(1366, 768), interpolation = cv2.INTER_CUBIC)
    frame=cv2.flip(frame1,1)
    lh=cv2.getTrackbarPos('Lower H','trackbars')
    hh=cv2.getTrackbarPos('Higher H','trackbars')
    ls=cv2.getTrackbarPos('Lower S','trackbars')
    hs=cv2.getTrackbarPos('Higher S','trackbars')
    lv=cv2.getTrackbarPos('Lower V','trackbars')
    hv=cv2.getTrackbarPos('Higher V','trackbars')
    #lower = np.array([50,100,40])
    #upper = np.array([102,255,249])
    lower = np.array([lh,ls,lv])
    upper = np.array([hh,hs,hv])
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(frameHSV,lower,upper)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    cv2.namedWindow('Result',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Result', 1366,768)
    cv2.imshow('Result',res)    

    k=cv2.waitKey(1)
    if k==ord('q'):
        break

    if k==ord('s'):
        set=1
        
    if(set==1):
        ret,cnts,heirarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if(len(cnts)==0):
            continue
        else:
            #cnts1=sorted(cnts,key=cv2.contourArea, reverse=True)[:5]
            #maxcnt=cnts1[0]
            #secondcnt=cnts[1]
            maxcnt = max(cnts,key=cv2.contourArea)
            epsilon = 0.1*cv2.arcLength(maxcnt,True)
            approx = cv2.approxPolyDP(maxcnt,epsilon,True)
            #epsilon1 = 0.1*cv2.arcLength(secondcnt,True)
            #approx1 = cv2.approxPolyDP(secondcnt,epsilon1,True)
            M = cv2.moments(approx)
            cv2.drawContours(frame,approx,-1,(0,255,0),2)
            
            if(M['m00']==0):
                continue
            else:
                
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])                                  
                cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)                               
                win32api.SetCursorPos((cx,cy))
                area=cv2.contourArea(approx)
                #area=cv2.contourArea(approx)
                print(cv2.contourArea(approx))
                if(area>850 and area<2000):                    
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cx1,cy1,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cx1,cy1,0,0)
                #area1=area
                cx1=cx
                cy1=cy
            cv2.drawContours(frame,approx,-1,(0,255,0),2)
            cv2.imshow('Track',frame)
               
cv2.destroyAllWindows()
cap.release()
