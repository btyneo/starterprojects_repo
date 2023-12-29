import torch
import torch.nn as nn
import numpy as np
import cv2 as cv
import torchvision.transforms as transform
import matplotlib.pyplot as plt
from torchvision.datasets import ImageFolder
import torch.nn.functional as F




#these directories contain folders for each (test and train); each of them have 7 folders inside
train_directory = "drive/MyDrive/datasets/fer2013/train"
test_directory = "drive/MyDrive/datasets/fer2013/test"
checkpoint = True
#we need to unload the images from each folder inside the directory and their labels accordingly. ALSO WE NEED TO APPLY TRANSFORM FUNCTION
#labels are given according to how the folders are arranged in the directory; 0 for angry, 1 for happy etc.
#we use ImageFolder(location, transform=) for this
#we use (64, 64) so all pics are of same size, and 64x64 is a good choice. normalization is to adjusting pixel values to a standard scale
#define important variables (lr, epochs etc) and then create model and define optimizer and loss
learning_rate = 0.001
num_epoch = 50
batch_size = 45 #since fer2013 isnt a big dataset, range from 32 to 64 for batch_size is good
transformtrain = transform.Compose([
    transform.Resize((64, 64)),
    transform.RandomHorizontalFlip(),  # Randomly flip images horizontally.
    transform.RandomRotation(10),       # Randomly rotate images by up to 10 degrees.
    transform.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transform.ToTensor(),
    transform.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])
transform = transform.Compose([transform.Resize((64, 64)), transform.ToTensor(), transform.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
train_dataset = ImageFolder(train_directory, transform=transformtrain) #saving dataset
test_dataset = ImageFolder(test_directory, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size = batch_size, shuffle=True) #loading dataset
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size = batch_size, shuffle=False)


#making the neural net//Convolutional because image classification. define the layers used and forward pass
# class emotion_neural_net(nn.Module):
#   def __init__(self, no_classes):
#     super(emotion_neural_net, self).__init__()
#     self.conv1 = nn.Conv2d(3, 16, 3, 1) #arguments for Conv2d are (color_channels, output_features, kernal, stride). u can change the last 3.
#     self.pool = nn.MaxPool2d(2, 2) #maxpooling layer downsizes the image sample. 2x2 in this case will be downsized.
#     #we chose 3 color channels because its RGB. 16 for output features because its typical. 3 for kernal and 1 for stride are usually good.
#     self.conv2 = nn.Conv2d(16, 32, 3, 1) #arguments are same; (input, output, kernal, stride)
#     #the num of features that we are using is basically the details from the image the model will learn, so we are increasing it
#     self.fc1 = nn.Linear(32 * 14 * 14, 128) #since we downsized the image so we will use (14, 14) as an estimate pixel & 32 features so multiply it
#     self.fc2 = nn.Linear(128, no_classes) #we want to output to the num of classes we have

#   def forward_pass(self, x):
#     out = self.pool(F.relu(self.conv1(x))) #applying max pooling and relu for each conv layer
#     out = self.pool(F.relu(self.conv2(out)))
#     #we need to flatten the output before putting it in the fc layer
#     out = out.view(-1, 32*14*14)
#     out = F.relu(self.fc1(out))
#     out = self.fc2(out)
#     return out

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


model = emotion_neural_net(7)
loss_calculator = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
def load_checkpoint():
  model.load_state_dict(torch.load("checkpoint1.pth.tar"))


# Set your model to evaluation mode if needed


# if checkpoint:
#   load_checkpoint()

model.eval()
#training loop
n_steps = len(train_loader)
for epoch in range(num_epoch):
  for i, (images, labels) in enumerate(train_loader):
    #forward pass and calculating loss
    output = model.forward_pass(images) #the label is the emotion, image is the data. we are trying to predict the label.
    loss = loss_calculator(output, labels) #arguments are (y_pred, y) where y_pred is the prediction of the emotion of the image.

    #backward pass and zero_grad

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (i+1) % 50 == 0:
      print(f"Epoch: {epoch+1}/{num_epoch}, step: {i}/{n_steps}, loss: {loss.item():.4f}")

print("Finished training.")


#testing data. we dont want to influence the gradient so we do it with no grad

with torch.no_grad():
  n_correct = 0
  n_samples = 0
  for images, labels in test_loader:
    outputs = model.forward_pass(images)
    ignore, predicted = torch.max(outputs, 1) #here the predicted is the predicted label for the image. torch.max() for highest probability
    n_samples += labels.size(0) #labels is a tensor containing truth labels for data, .size(0) gets the num of elements in first dimension
    n_correct += (predicted == labels).sum().item()

  accuracy = 100.0 * n_correct/n_samples
  print(f"Accuracy: {accuracy:.2f}%")


torch.save(model.state_dict(), "checkpoint2.pth.tar")


