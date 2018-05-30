import cv2
import time

save_path = 'C:\\Users\\a2001\\Desktop\\' #ex: 'C:\\Users\\username\\Desktop\\saved_faces'
cascade = 0 #0 for Haar; 1 for LBP

if (cascade == 0):
    face_cascade = cv2.CascadeClassifier('haarcascades\\haarcascade_frontalface_alt.xml')
elif (cascade == 1):
    face_cascade = cv2.CascadeClassifier('lbpcascades\\lbpcascade_frontalface.xml')
    
autoSave = False #autosave pictures when faces detected
markOn = False #leave the detection mark
webcamOn = True #True for webcam; False for video
if(webcamOn):
    cap = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture('..\\database\\image recognition\\examples\\footage.mp4')

blockColor = [
        (255, 0, 0), #0:blue
        (0, 255, 0), #1:green
        (0, 0, 255), #2:red
        (255, 255, 0), #3:teal
        (0, 255, 255), #4:orange
        (255, 0, 255) #5:purple
        ]

def faceDetection(name):
    isOn = True
    while(True):
        if(webcamOn):
            ret, frame = cap.read()
        else:
            ret, frame = vid.read()
            if (not ret):
                break
        keypress = cv2.waitKey(1)
        
        if(ret is True):
            if(not webcamOn):
                frame = cv2.resize(frame, None, fx=0.3, fy=0.3, interpolation = cv2.INTER_LINEAR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            date = time.strftime('%Y%m%d_%H%M%S')
            
            for (x,y,w,h) in faces:
                display = frame.copy()
                i = 1
                cv2.rectangle(frame, (x,y), (x+w, y+h), blockColor[i], 2)
                
                #auto-save
                if(autoSave):
                    mes = 'Faces found: ' + str(len(faces))    
                    print(mes)
                    if (markOn):
                        cv2.imwrite((save_path+'saved_faces_'+date+'.jpg'), frame)
                    else:
                        cv2.imwrite((save_path+'saved_faces_'+date+'.jpg'), display)
                    
                    #file saved
                    text = 'File saved'
                    boxColor = (200, 255, 200)
                    textColor = (0, 255, 0)
                    textBox(frame, text, boxColor, textColor)

                                    
            #quit
            if keypress & 0xFF == ord('q'):  
                break        
            
            #print the number of faces found
            if (len(faces) > 0):
                mes = 'Faces found: ' + str(len(faces))    
                
                #pause
                if keypress & 0xFF == ord(' '):
                    isOn = not isOn
                    if (not isOn and autoSave == False):
                        print(mes)
                        if (markOn):
                            cv2.imwrite((save_path+'saved_faces_'+date+'.jpg'), frame)
                        else:
                            cv2.imwrite((save_path+'saved_faces_'+date+'.jpg'), display)
                        
                        #file saved
                        text = 'File saved'
                        boxColor = (200, 255, 200)
                        textColor = (15, 15, 15)
                        textBox(frame, text, boxColor, textColor)
                        cv2.imshow(name, frame)
                
                #print instruction
                if (not autoSave):
                    text = 'Press \'Space\' to screenshot/Press \'q\' to quit'
                    boxColor = (235, 235, 235)
                    textColor = (15, 15, 15)
                    textBox(frame, text, boxColor, textColor)
                
            else:
                #pause
                if keypress & 0xFF == ord(' '):
                    isOn = not isOn
                    
                #detection error
                text = 'Detection Error: objects(faces) not found'
                mes = text                
                boxColor = (200, 200, 255)
                textColor = (0, 0, 255)
                textBox(frame, text, boxColor, textColor)
               
        else:
            continue
        
        if(isOn):
            cv2.imshow(name, frame)
    
    if(webcamOn):
        cap.release()
    else:
        vid.release()            
    cv2.destroyAllWindows()
    
def textBox(frame, text, boxColor, textColor):
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = (frame.shape[1] * 0.8) / frame.shape[1]
    thickness = 1
    #get boundary of the text
    textsize = cv2.getTextSize(text, font, size, thickness)[0]
    #get coords
    textX = int((frame.shape[1] - textsize[0]) / 2)
    textY = frame.shape[0] - textsize[1] * 2
    textXa = textX
    textXb = textX + textsize[0]
    overlay = frame.copy()
    cv2.rectangle(overlay, (textXa-3, textY-int(textsize[1]*0.5)), (textXb+3, textY+int(textsize[1]*1.5)), boxColor, -1)
    cv2.putText(overlay, text, (textXa, textY+15), font, size, textColor, thickness)
    opacity = 0.7
    cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

faceDetection('Output')