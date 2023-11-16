import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random
from win32com.client import Dispatch

detector=HandDetector(detectionCon=0.9, maxHands=2)

video=cv2.VideoCapture(0)

def speak(str1, rate=0):
    speak = Dispatch("SAPI.SpVoice")
    speak.Rate = rate
    speak.Speak(str1)

def selfie(timer):
    prev=time.time()
    while timer>=0:
        ret,frame=video.read()
        cv2.rectangle(frame,(0,0),(190,50),(0,0,0),-2,cv2.LINE_AA)
        cv2.putText(frame, 'Timer : {}'.format(str(timer)), (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (225,225,225), 2)
        cv2.imshow('frame',frame)
        cv2.waitKey(100)
        cur=time.time()
        if cur-prev>1:
            prev=cur
            timer=timer-1
    else:
        ret,frame=video.read()
        cv2.imshow('frame',frame)
        cv2.waitKey(1000)
        cv2.imwrite("camera{}.jpg".format(random.randint(1,1000)),frame)

while True:
    ret, frame=video.read()
    hands, _ = detector.findHands(frame)
    if hands:
        hands1=hands[0]
        fingercount = detector.fingersUp(hands1)
        print(fingercount)            
        if fingercount==[0,1,1,1,0]:
            selfie(int(3))
            speak("Beap..",rate=100)
        if fingercount==[1,1,1,1,1]:
            selfie(int(5))
            speak("Beap..",rate=100)
        if fingercount==[0,0,0,0,0]:
            speak("Goodbye..",rate=2)
            break

    cv2.imshow('frame', frame)
    q=cv2.waitKey(1)
    if q == ord('e'):
        break

video.release()
cv2.destroyAllWindows()