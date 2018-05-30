import cv2

image_path = 'faces\\'
cascade = 0 #0 for Haar; 1 for LBP

if (cascade == 0):
    face_cascade = cv2.CascadeClassifier('haarcascades\\haarcascade_frontalface_alt.xml')
elif (cascade == 1):
    face_cascade = cv2.CascadeClassifier('lbpcascades\\lbpcascade_frontalface.xml')

def faceDetection(name, mypicture):
    img = cv2.imread(mypicture)
    if (img is None):
        print('Import Error: image not found')
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)
    #print the number of faces found
    if (len(faces) > 0):    
        print(name, ':\nFaces found: ', len(faces))
    else:
        #detection error
        text = 'Detection Error: objects(faces) not found'
        mes = text
        print(mes)                
        boxColor = (200, 200, 255)
        textColor = (0, 0, 255)
        textBox(img, text, boxColor, textColor)
        cv2.imshow(name, img)        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return
    
    #recognize face; return size of object
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (100,255,100), 2)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
        
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def textBox(img, text, boxColor, textColor):
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = (img.shape[1] * 0.5) / img.shape[1]
    thickness = 1
    #get boundary of the text
    textsize = cv2.getTextSize(text, font, size, thickness)[0]
    #get coords
    textX = int((img.shape[1] - textsize[0]) / 2)
    textY = img.shape[0] - textsize[1] * 2
    textXa = textX
    textXb = textX + textsize[0]
    overlay = img.copy()
    cv2.rectangle(overlay, (textXa-3, textY-int(textsize[1]*0.5)), (textXb+3, textY+int(textsize[1]*2)), boxColor, -1)
    cv2.putText(overlay, text, (textXa, textY+15), font, size, textColor, thickness)
    opacity = 0.7
    cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    
for i in range(1, 6):
    i = str(i)
    faceDetection('test'+i, (image_path + 'test'+i+'.jpg'))