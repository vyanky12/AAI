from time import time
from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone

####################################
classID = 0  # 0 is fake and 1 is real
outputFolderPath = 'Dataset/all/DataCollect'
confidence = 0.8
save = True
blurThreshold = 35  # Larger is more focused

debug = False
offsetPercentageW = 10
offsetPercentageH = 20
camWidth, camHeight = 640, 480
floatingPoint = 6
####################################

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the FaceDetector object
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Initialize lists
listBlur = []  # True/False values indicating if the faces are blurred or not
listInfo = []  # The normalized values and the class name for the label text file

# Run the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    success, img = cap.read()

    # Detect faces in the image
    img, bboxs = detector.findFaces(img, draw=False)

    # Check if any face is detected
    if bboxs:
        # Loop through each bounding box
        for bbox in bboxs:
            x, y, w, h = bbox['bbox']
            print(x, y, w, h)
            score = int(bbox['score'][0] * 100)

            # Draw Data
            #cvzone.putTextRect(img, f'{score}%', (x, y - 10))
            #cvzone.cornerRect(img, (x, y, w, h))

            # Check the score
            if score > confidence:
                # Adding an offset to the face detected
                offsetW = (offsetPercentageW / 100) * w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)
                offsetH = (offsetPercentageH / 100) * h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                # To avoid values below 0
                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

                # Find Blurriness
                imgFace = img[y:y + h, x:x + w]
                cv2.imshow("Face", imgFace)
                blurValue = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
                listBlur.append(blurValue > blurThreshold)

                # Normalize Values
                ih, iw, _ = img.shape
                xc, yc = x + w / 2, y + h / 2

                xcn, ycn = round(xc / iw, floatingPoint), round(yc / ih, floatingPoint)
                wn, hn = round(w / iw, floatingPoint), round(h / ih, floatingPoint)

                # To avoid values above 1
                if xcn > 1: xcn = 1
                if ycn > 1: ycn = 1
                if wn > 1: wn = 1
                if hn > 1: hn = 1

                listInfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n")

                # Drawing
                cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 3)
                cvzone.putTextRect(img, f'Score: {score}% Blur: {blurValue}', (x, y - 0),
                                   scale=2, thickness=3)
                if debug:
                    cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 3)
                    cvzone.putTextRect(img, f'Score: {score}% Blur: {blurValue}', (x, y - 0),
                                       scale=2, thickness=3)

        # To Save
        if save and all(listBlur):
            timeNow = time()
            timeNow = str(timeNow).split('.')
            timeNow = timeNow[0] + timeNow[1]
            cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg", img)
            for info in listInfo:
                with open(f"{outputFolderPath}/{timeNow}.txt", 'a') as f:
                    f.write(info)
                    f.close()

    # Display the image in a window named 'Image'
    cv2.imshow("Image", img)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
