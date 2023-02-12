#THANK YOU JESUS
#PLEASE HELP ME LORD

#IMPORT THE NECESSARY MODULES
import cv2
import cvzone
import mediapipe as mp
import time
import numpy as np
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
#CREATING THE KEYBOARD KEYS
class Keys():
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def drawall(self, screen, text_color=(255, 255, 255), bg_color=(0, 0, 0), alpha=0.5, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2):
        rec = screen[self.y: self.y + self.height, self.x: self.x + self.width]
        rect = np.ones(rec.shape, dtype=np.uint8)  # * 25
        rect[:] = bg_color
        res = cv2.addWeighted(rec, alpha, rect, 1 - alpha, 1.0)
        res = screen[self.y: self.y + self.height, self.x: self.x + self.width]  # resetting the screen
        text_size = cv2.getTextSize(self.text, fontFace, fontScale, thickness)
        text_position = (int(self.x + self.width / 2 - text_size[0][0] / 2), int(self.y + self.height / 2 + text_size[0][1] / 2))
        cv2.putText(screen, self.text, text_position, fontFace, fontScale, text_color, thickness)

    def func(self, x, y):
        if (self.x + self.width > x > self.x) and (self.y + self.height > y > self.y):
            return True
        return False


class handtracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands

        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, screen, draw=True):
        image = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(screen, handLm, self.mpHands.HAND_CONNECTIONS)
        return screen

    def getPostion(self, screen, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = screen.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(screen, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lmList

def Distance(pt1, pt2):
    return int(((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5)

width, height = 80, 60
X, Y = 40, 200
keyboard_keys =[]
letters = list("1234567890QWERTYUIOPASDFGHJKLZXCVBNM ")
for letter, l in enumerate(letters):
    if letter < 10:
        keyboard_keys.append(Keys(X + letter * width + letter * 5, Y, width, height, l))
    elif letter < 20:
        keyboard_keys.append(Keys(X + (letter -10) * width + letter * 5, Y + height + 5, width, height, l))
    elif letter < 29:
        keyboard_keys.append(Keys(X + (letter - 20) * width + letter * 5, Y + 2 * height + 10, width, height, l))
    elif letter <37:
        keyboard_keys.append(Keys(X + (letter - 30) * width + letter * 5, Y + 3 * height + 15, width, height, l))

keyboard_keys.append(Keys(X + 250, Y + 4 * height + 15, 5 * width, height, "Space Bar"))
#keyboard_keys.append(Keys((X - width) - 70, Y + 2 * height + 10, 5 * width, height, "clear"))
keyboard_keys.append(Keys(X + 7 * width + 60, Y + 3 * height + 15, 5 * width, height, "backspace"))

dialog_box = Keys(X, Y - height - 5, 10 * width + 9 * 5, height, '')


hand_trac_ker = handtracker()

Ctrl = Controller()
ClickedX = 0
ClickedY = 0
screen_f_Height, screen_f_Width, _ = cap.read()[1].shape

prevclick = 0
show = True
while True:
    signTipX = 0
    signTipY = 0

    thumbTipX = 0
    thumbTipY = 0

    ttt, screen_f = cap.read()
    if not ttt:
        break

    screen_f = cv2.resize(screen_f, (int(screen_f_Width * 1.5), int(screen_f_Height * 1.5)))
    screen_f = cv2.flip(screen_f, 1)
    # find hands
    screen_f = hand_trac_ker.findHands(screen_f)
    lmList = hand_trac_ker.getPostion(screen_f, draw=False)
   # l, _, _ = hand_detector.findDistance(8, 12, screen_f)
    if lmList:
        signTipX, signTipY = lmList[12][1], lmList[12][2]
        thumbTipX, thumbTipY = lmList[4][1], lmList[4][2]
        if Distance((signTipX, signTipY), (thumbTipX, thumbTipY)) < 0.0005:
            centerX = int((signTipX + thumbTipX) / 2)
            centerY = int((signTipY + thumbTipY) / 2)
            cv2.line(screen_f, (signTipX, signTipY), (thumbTipX, thumbTipY), (0, 255, 0), 2)
            cv2.circle(screen_f, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

        ctime = time.time()
        alpha = 0.5
        dialog_box.drawall(screen_f, (255, 255, 255), (0, 0, 0), 0.3)
        if show:
            # dialog_box.drawall(screen_f, (255, 255, 255), (0, 0, 0), 0.3)
            for each_key in keyboard_keys:
                if each_key.func(signTipX, signTipY):
                    alpha = 0.1

                    if each_key.func(thumbTipX, thumbTipY):
                        ctime = time.time()
                        if ctime - prevclick > 0.4:

                            if each_key.text == 'backspace':
                                dialog_box.text = dialog_box.text[:-1]
                                #each_key.text = each_key.text[:-1]
                                time.sleep(1)
                            elif each_key.text == 'clear':
                                dialog_box.text = ''
                                time.sleep(1)
                            elif len(dialog_box.text) < 30:
                                if each_key.text == 'Space Bar':
                                    dialog_box.text += " "
                                    #each_key.text += " "
                                    time.sleep(1)
                                else:
                                    dialog_box.text += each_key.text
                                # simulating the press of actuall keyboardE
                                    Ctrl.press(each_key.text)
                                    time.sleep(1)



                            #previousClick = ctime
                each_key.drawall(screen_f, (255, 255, 255), (0, 0, 0), alpha=alpha)
                alpha = 0.5


        ptime = ctime

    cv2.imshow('camera', screen_f)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()