import cv2,csv

WINDOW_ID = '0x4200009'  # minecraftのwindowのID, ``xwininfo | grep 'Window id'``
WIDTH=1000
HEIGHT=1000

#video = cv2.VideoCapture(f'ximagesrc xid={WINDOW_ID} ! videoconvert ! appsink')
video = cv2.VideoCapture(f'ximagesrc xid={WINDOW_ID} ! videoconvert ! videoscale ! video/x-raw,width={WIDTH},height={HEIGHT} ! appsink')

list = []

while True:
    try :
        ok, img = video.read()
        if not ok:
            break
        height, width = img.shape[:2] # max_height=1145 max_width=1853

        center_from_x = (int)(width/2) - 1
        center_from_y = (int)(height/2) - 1
        center_to_x   = (int)(width/2) + 1
        center_to_y   = (int)(height/2) + 1
        imgBox = img[center_from_y: center_to_y, center_from_x: center_to_x]

        # Get mean of RGB
        b = imgBox.T[0].flatten().mean()
        g = imgBox.T[1].flatten().mean()
        r = imgBox.T[2].flatten().mean()

        print(r, end=',')
        print(g, end=',')
        print(b)

        if [r, g, b] not in list:
            list.append([r, g, b])

        #cv2.imshow('test', img)
    except :
        result_file = open("output.csv",'wb')
        with open('output.csv','w') as result_file:
            wr = csv.writer(result_file)
            for row in list:
                wr.writerow(row)
        break
