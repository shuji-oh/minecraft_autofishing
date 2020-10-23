import cv2,csv,time
import pandas as pd
from pynput.mouse import Button, Controller 

WINDOW_ID = '0x4200009'  # minecraftのwindowのID, ``xwininfo | grep 'Window id'``
WIDTH=1000
HEIGHT=1000

video = cv2.VideoCapture(f'ximagesrc xid={WINDOW_ID} ! videoconvert ! videoscale ! video/x-raw,width={WIDTH},height={HEIGHT} ! appsink')

df = pd.read_csv('output.csv', sep=',', encoding='utf-8', index_col=False, header=None)
list = df.values.tolist()

suspicious_counter = 0

mouse = Controller()

while True:
    ok, img = video.read()
    if not ok:
        break
    height, width = img.shape[:2]

    center_from_x = (int)(width/2) - 1
    center_from_y = (int)(height/2) - 1
    center_to_x   = (int)(width/2) + 1
    center_to_y   = (int)(height/2) + 1
    imgBox = img[center_from_y: center_to_y, center_from_x: center_to_x]

    # Get mean of RGB
    b = imgBox.T[0].flatten().mean()
    g = imgBox.T[1].flatten().mean()
    r = imgBox.T[2].flatten().mean()

    # detect fishing event
    if [r, g, b] not in list:
        suspicious_counter += 1
    else :
        suspicious_counter = 0

    if suspicious_counter >= 13:
        print("fishing.")
        mouse.click(Button.right, 1)
        time.sleep(2)
        mouse.click(Button.right, 1)
        time.sleep(2)
        suspicious_counter = 0
 
    #cv2.imshow('test', img)
