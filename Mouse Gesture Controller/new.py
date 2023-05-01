

# PRESS ESC BUTTON TO EXIT


try:
    import mediapipe
    import cv2
    import pyautogui
    import math
    import traceback
    import mouse
    import datetime
    capture = cv2.VideoCapture(0)
    fw = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    fh = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    sw, sh= pyautogui.size()
    
    def show(i):
        if i is not None:
            coor = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(i.x,i.y,fw,fh)
            if coor is not None:
                cv2.putText(frame,str(coor),(coor[0]+20,coor[1]+20),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0, 0), 2)
                return list(coor)
    
    def makeline(i1,i2,i3):
        ci1 = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(i1.x,i1.y,fw,fh)
        ci2 = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(i2.x,i2.y,fw,fh)
        ci3 = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(i3.x,i3.y,fw,fh)
        cv2.line(frame,ci1,ci2,(0,0,255),5)
        cv2.line(frame,ci2,ci3,(0,0,255),5)
        cv2.line(frame,ci1,ci3,(0,0,255),5)
        return frame
        
    def scale(coord):
        x1,y1=coord[0]*(sw/fw)-(sw/2),coord[1]*(sh/fh)-(sh/2)
        x2,y2=(x1*1.8)+(sw/2),(y1*1.8)+(sh/2)
        return (round(x2),round(y2))
    
    def ratio(a,b,c):
        mean=(math.dist(a,b)+math.dist(a,c))/2
        r= mean/math.dist(b,c)
        if r>3:
            return [1,r]
        else:
            return [0,r]
        
    def mp(a,b):
        x=int((a[0]+b[0])/2)
        y=int((a[1]+b[1])/2)
        return (x-20,y-20)
        
    
    with mediapipe.solutions.hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
        clicked=0
        cin=[0,0]
        t1=datetime.datetime.now()
        while capture.isOpened():
            ret, frame = capture.read()
            if ret == False:
                continue
            frame = cv2.flip(frame, 1)
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks != None:
                index = results.multi_hand_landmarks[0].landmark[mediapipe.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                thumb=results.multi_hand_landmarks[0].landmark[mediapipe.solutions.hands.HandLandmark.THUMB_TIP]
                little=results.multi_hand_landmarks[0].landmark[mediapipe.solutions.hands.HandLandmark.PINKY_TIP]
                cindex=show(index)
                cthumb=show(thumb)
                clittle=show(little)
                if cthumb is not None and clittle is not None and cindex is not None:
                    a=scale(cindex)
                    b=scale(cthumb)
                    c=scale(clittle)
                    if math.dist(a,cin)>5:
                        mouse.move(a[0], a[1])
                        cin=a
                    t2=datetime.datetime.now()
                    if ratio(a,b,c)[0]==1 and clicked==0 and int((t2-t1).total_seconds() * 1000)>500:
                        mouse.click("left")  
                        clicked=1
                        t1=datetime.datetime.now()
                    else:
                        clicked=0
                    frame=makeline(index,thumb,little)
                    cv2.putText(frame,str(round(math.dist(b,c))),mp(cthumb,clittle),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 2)
                    cv2.putText(frame,str(round(math.dist(a,c))),mp(cindex,clittle),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 2)
                    cv2.putText(frame,str(round(math.dist(a,b))),mp(cindex,cthumb),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 2)
                    cv2.putText(frame,"Ratio:- "+str(round(ratio(a,b,c)[1],2)),(20, 70),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 2)
            cv2.imshow('Mouse Controller', frame)
            if cv2.waitKey(1) == 27: #escape key
                break
    cv2.destroyAllWindows()
    capture.release()

except:
    cv2.destroyAllWindows()
    capture.release()
    traceback.print_exc()
    
    
# PRESS ESC BUTTON TO EXIT
