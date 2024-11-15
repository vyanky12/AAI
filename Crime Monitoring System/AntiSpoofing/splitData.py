import os
import random
import shutil
from itertools import islice

outputFolderPath = "Dataset/SplitData"
inputFolderPath = "Dataset/all/DataCollect"  # Adjust this if needed
splitRatio = {"train": 0.7, "val": 0.2, "test": 0.1}
classes = ["fake", "real"]

# Clean up the output directory
try:
    shutil.rmtree(outputFolderPath)
except OSError:
    pass  # Ignore if the directory does not exist

# Create necessary directories
os.makedirs(f"{outputFolderPath}/train/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/train/labels", exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/labels", exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/labels", exist_ok=True)

# Get unique names of files (excluding extensions)
listNames = os.listdir(inputFolderPath)

uniqueNames = []
for name in listNames:
    if name.endswith(('.jpg', '.png')):  # Only consider valid image files
        uniqueNames.append(name.split('.')[0])  # Extract the name without extension

uniqueNames = list(set(uniqueNames))  # Remove duplicates

# Shuffle the names
random.shuffle(uniqueNames)

# Determine the number of images for each dataset split
lenData = len(uniqueNames)
lenTrain = int(lenData * splitRatio['train'])
lenVal = int(lenData * splitRatio['val'])
lenTest = int(lenData * splitRatio['test'])

# Adjust training set size if necessary
if lenData != lenTrain + lenTest + lenVal:
    remaining = lenData - (lenTrain + lenTest + lenVal)
    lenTrain += remaining

# Split the list
lengthToSplit = [lenTrain, lenVal, lenTest]
Input = iter(uniqueNames)
Output = [list(islice(Input, elem)) for elem in lengthToSplit]
print(f'Total Images: {lenData} \nSplit: {len(Output[0])} {len(Output[1])} {len(Output[2])}')

# Copy the files to the new directories
sequence = ['train', 'val', 'test']
for i, out in enumerate(Output):
    for fileName in out:
        # Define source file paths
        img_src = f'{inputFolderPath}/{fileName}.jpg'
        lbl_src = f'{inputFolderPath}/{fileName}.txt'

        # Safely copy image and label files if they exist
        if os.path.exists(img_src):
            shutil.copy(img_src, f'{outputFolderPath}/{sequence[i]}/images/{fileName}.jpg')
        else:
            print(f"Image file not found: {img_src}")

        if os.path.exists(lbl_src):
            shutil.copy(lbl_src, f'{outputFolderPath}/{sequence[i]}/labels/{fileName}.txt')
        else:
            print(f"Label file not found: {lbl_src}")

print("Split Process Completed...")

# Create data.yaml file
dataYaml = f'path: ../Data\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}'

with open(f"{outputFolderPath}/data.yaml", 'w') as f:
    f.write(dataYaml)

print("Data.yaml file Created...")
