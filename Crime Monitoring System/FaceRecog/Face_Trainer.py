import cv2  # For Image processing
import numpy as np  # For converting Images to Numerical array
import os  # To handle directories
from PIL import Image  # Pillow lib for handling images

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_crqeate()  # Updated method for OpenCV

Face_ID = -1
prev_person_name = ""
y_ID = []
x_train = []
name_dict = {}  # Dictionary to store Face_ID to name mapping

Face_Images = os.path.join(os.getcwd(), "Face_Images")  # Directory containing the face images
print(Face_Images)

for root, dirs, files in os.walk(Face_Images):  # Go to the face image directory
    for file in files:  # Check every directory in it
        if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png"):  # For image files ending with jpeg, jpg or png
            path = os.path.join(root, file)
            person_name = os.path.basename(root)  # Get the name from the directory name
            print(path, person_name)

            if prev_person_name != person_name:  # Check if the name of person has changed
                Face_ID += 1  # If yes, increment the ID count
                prev_person_name = person_name
                name_dict[Face_ID] = person_name  # Map Face_ID to the person's name

            Gery_Image = Image.open(path).convert("L")  # Convert the image to greyscale using Pillow
            Crop_Image = Gery_Image.resize((800, 800), Image.LANCZOS)  # Resize the Grey Image
            Final_Image = np.array(Crop_Image, "uint8")
            faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.5, minNeighbors=5)  # Detect faces
            print(Face_ID, faces)

            for (x, y, w, h) in faces:
                roi = Final_Image[y:y+h, x:x+w]  # Crop the Region of Interest (ROI)
                x_train.append(roi)
                y_ID.append(Face_ID)

# Train the model
recognizer.train(x_train, np.array(y_ID))  # Create a Matrix of Training data
recognizer.save("face-trainner.yml")  # Save the matrix as YML file

# Save the name dictionary for later use
with open("name_dict.txt", "w") as f:
    for fid, name in name_dict.items():
        f.write(f"{fid}:{name}\n")  # Save the mapping to a file
