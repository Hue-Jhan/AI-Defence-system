import cv2, os

video=cv2.VideoCapture(0)
save_dir = "...datasets..." # insert dir
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

if not video.isOpened():
    print("Error: Could not open camera.")
    exit()

cascade_path = r"models\haarcascade_frontalface_default.xml"
facedetect = cv2.CascadeClassifier(cascade_path)

id = input("Enter Your ID: ")
count=0

while True:

    ret,frame=video.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        count=count+1
        cv2.imwrite(os.path.join(save_dir, 'User.'+str(id)+"."+str(count)+".jpg"), gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        print("a ")

    cv2.imshow("Frame",frame)
    k=cv2.waitKey(1)
    if count>500:
        break

video.release()
cv2.destroyAllWindows()
print("Dataset Collection Done")
