import cv2  # For image processing
import numpy as np  # For numerical operations

# Load the face detection and recognition models
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face-trainner.yml")  # Load the trained model

# Load the name dictionary
name_dict = {}
with open("name_dict.txt", "r") as f:
    for line in f.readlines():
        fid, name = line.strip().split(":")
        name_dict[int(fid)] = name  # Convert Face_ID to int and store the name

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)
verified_persons = set()  # To keep track of verified persons

while True:
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w]  # Get the Region of Interest (ROI)
        label, confidence = recognizer.predict(roi_gray)  # Predict the label and confidence

        # Print "Person Verified" if confidence is below 100%
        if confidence >=85 :  # Adjust the threshold as necessary
            person_name = name_dict.get(label, "Unknown")
            if person_name not in verified_persons:  # Check if person is already verified
                print(f"Person Verified: {person_name} (Confidence: {confidence:.2f})")
                verified_persons.add(person_name)  # Add to verified persons
            color = (0, 255, 0)  # Green for verified
        else:
            person_name = "Unknown"
            print(f"Person Not Verified (Confidence: {confidence:.2f})")
            color = (0, 0, 255)  # Red for unknown

        # Draw rectangle around the face and put text
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, person_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Display the resulting frame
    cv2.imshow("Face Recognition", frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
