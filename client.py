import socket
import cv2     # Open cv-python used to read video
import pickle  # convert python objects to byte stream
import struct
import mediapipe as mp
from time import ctime, time
import time
import os
import HandTrackingModule as htm
from cv2 import INTER_AREA
import pyttsx3
engine = pyttsx3.init('sapi5')
engine.setProperty("rate", 120)
voices = engine.getProperty("voices")

engine.setProperty("voices", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# creating socket for connection
'192.168.214.31'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.56.1'
port = 9999
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

# ----------------
detector = htm.handDetector(detectionCon=0)

tipIds = [4, 8, 12, 16, 20]  # thumb , index , middle , ring , pinky
totalFingers = 0
flag = False

detect = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# -------------------------------
ct = 0
guessedText = ""
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    # ---------------------
    img = frame
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        Rfingers = []
        Lfingers = []

        # Right hand
        if lmList[tipIds[0]][1] > lmList[tipIds[4]][1]:
            # thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                Rfingers.append(1)
            else:
                Rfingers.append(0)

            # 4 Rfingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    Rfingers.append(1)
                else:
                    Rfingers.append(0)

            if Rfingers == [1, 1, 1, 1, 1]:
                if (detect[0] == 0):
                    print("Hello, how are you?")
                    speak("Hello, how are you?")
                    guessedText = "Hello, how are you?"
                    flag = True
                    detect[0] = 1

            elif Rfingers == [1, 0, 0, 0, 0]:
                if (detect[0] == 0):
                    print("I'm good, thanks!")
                    speak("I'm good, thanks!")
                    guessedText = "I'm good, thanks!"
                    flag = True
                    detect[0] = 1

            elif Rfingers == [1, 1, 0, 0, 1]:
                if (detect[1] == 0):
                    guessedText = "Yo bro!!"
                    print("Yo bro!!")
                    speak("Yo bro!!")
                    flag = True
                    detect[1] = 1

            elif Rfingers == [0, 1, 1, 0, 0]:
                if detect[2] == 0:
                    guessedText = "Peace"
                    print("Peace")
                    speak("Peace")
                    flag = True
                    detect[2] = 1
            elif Rfingers == [0, 0, 1, 1, 1]:
                if detect[6] == 0:
                    guessedText = "Super"
                    print("Super")
                    speak("Super")
                    flag = True
                    detect[6] = 1
            elif Rfingers == [1, 0, 0, 0, 1]:
                if detect[8] == 0:
                    guessedText = "Cool"
                    print("Cool")
                    speak("Cool")
                    flag = True
                    detect[8] = 1
            # cv2.rectangle(img, (28, 225), (170, 423), (0, 255, 0), cv2.FILLED)

        # Left Hand
        elif lmList[tipIds[0]][1] < lmList[tipIds[4]][1]:
            # thumb
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                Lfingers.append(1)
            else:
                Lfingers.append(0)

            # 4 Rfingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    Lfingers.append(1)
                else:
                    Lfingers.append(0)

            if Lfingers == [1, 1, 1, 1, 1]:
                if (detect[3] == 0):
                    print("Bye Bye")
                    speak("Bye Bye")
                    guessedText = "Bye Bye"
                    flag = True
                    detect[3] = 1

            elif Lfingers == [1, 1, 0, 0, 1]:
                if (detect[4] == 0):
                    guessedText = "Come let's play badminton"
                    print("Come let's play badminton")
                    speak("Come let's play badminton")
                    flag = True
                    detect[4] = 1

            elif Lfingers == [1, 1, 1, 0, 0]:
                if detect[5] == 0:
                    guessedText = "Let's have lunch in GJB"
                    print("Let's have lunch in GJB")
                    speak("Let's have lunch in GJB")
                    flag = True
                    detect[5] = 1
            elif Lfingers == [1, 0, 1, 1, 1]:
                if detect[7] == 0:
                    guessedText = "How is college life"
                    print("How is college life")
                    speak("How is college life")
                    flag = True
                    detect[7] = 1
        cv2.putText(img, guessedText, (100, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        ct += 1
        if (ct >= 100):
            ct = 0
            for i in range(len(detect)):
                detect[i] = 0
    # fps = 40

    # cv2.putText(img, f"FPS: {int(fps)}", (400, 70),
    #             cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
client_socket.close()
