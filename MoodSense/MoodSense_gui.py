import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import abc
import torch
import torch.nn as nn
import numpy as np
import cv2
import matplotlib.pyplot as plt
from torchvision.datasets import ImageFolder


class emotion_neural_net(nn.Module):
    def __init__(self, no_classes):
        super(emotion_neural_net, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, 1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, 3, 1)
        self.bn3 = nn.BatchNorm2d(128)
        self.fc1 = nn.Linear(128 * 6 * 6, 256)
        self.fc2 = nn.Linear(256, no_classes)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)  # Add dropout with 50% probability

    def forward_pass(self, x):
        out = self.pool(F.relu(self.bn1(self.conv1(x))))
        out = self.pool(F.relu(self.bn2(self.conv2(out))))
        out = self.pool(F.relu(self.bn3(self.conv3(out))))
        out = out.view(-1, 128 * 6 * 6)
        out = F.relu(self.fc1(out))
        out = self.dropout(out)
        out = self.fc2(out)
        return out


emotions = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Sad",
    5: "Surprise",
    6: "Neutral"
}
cap = cv2.VideoCapture(0)

cascade_location = r"C:\Users\hamza\Downloads\2023StarterProjects\Lib\site-packages\cv2\data\\"
face_cascade = cv2.CascadeClassifier(cascade_location + "haarcascade_frontalface_default.xml")

# loading trained emotiondetection model
model = emotion_neural_net(7)
checkpoint = torch.load("checkpoint1.pth.tar")
model.load_state_dict(checkpoint)
model.eval()
frame_counter = 0
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ret:
        break

    faces = face_cascade.detectMultiScale(grayscale_frame, 1.03, 14, minSize=(100, 100), maxSize=(240, 240)) #limiting it to detecting 1 face only
    for (x, y, w, h) in faces:
        # draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), color=(255, 166, 200), thickness=1)

        # extract face and put it through trained model. we need to make some changes to the frame of the face to pass it to our model
        face_frame = rgb_frame[y:y+h, x:x+w]
        face_frame = cv2.resize(face_frame, (64, 64))
        face_frame = transforms.ToTensor()(
            face_frame)  # transforms.ToTensor() is a function and we put argument outside it

        # making predictions
        if frame_counter == 0 or (frame_counter % 170) == 0:
            output = model.forward_pass(face_frame.unsqueeze(0))
            emotion_predicted = torch.argmax(output).item()  # .item() to remove it saying 'tensors' etc and give value only
            output_probabilities = torch.softmax(output, dim=1)
            emotion_probabilities = output_probabilities[0].tolist()

        #showing the detected emotions
        #this rectangle coordinates are for the box that'll show the emotions
        x_start = x + w + 20
        x_end = x + w + 220
        y_start = y - 20
        y_end = y+ h + 60
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 0, 0), -1)  # -1 fills the rectangle
        #showing the text
        i = 0
        y_gap = 40
        color = (173, 170, 162)
        coloruse = (0, 0, 0)
        detected_color = (0, 255, 0)
        for y, emotion in enumerate(emotion_probabilities):

            loading_bar_width = int(emotion * 100)
            if i > 6:
                i = 0
            if y == emotion_predicted:
                coloruse = detected_color
            else:
                coloruse = color
            cv2.putText(frame, f"{emotions[i]}: ", (x_start + 20, y_start+y_gap), cv2.FONT_ITALIC, 0.6, coloruse, 1)
            cv2.rectangle(frame, (x_start + 110, y_start + y_gap - 10),
                          (x_start+ 110 + loading_bar_width, y_start + y_gap + 2), (255, 166, 200), -1)
            # cv2.rectangle(frame, (x_start + 50, y_start+y_gap), (x_start + loading_bar_width, y_start+y_gap), (255, 166, 200), -1)
            i += 1
            y_gap += 25


    cv2.imshow('MoodSense | HamTech', frame)

    if cv2.waitKey(1) == 27:  # 27 corresponds to 'esc'
        break

cap.release()
cv2.destroyAllWindows()
