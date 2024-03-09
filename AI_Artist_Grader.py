import torch
from torchvision import transforms, models
from torchvision.models.efficientnet import EfficientNet_B0_Weights
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
import os
from PIL import Image
import yaml

def load_class_mapping(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return {str(cls): idx for idx, cls in enumerate(yaml_content['classes'])}

from torchvision.datasets import ImageFolder

class CustomDataset(ImageFolder):
    def __init__(self, root, transform=None):
        super().__init__(root, transform)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

current_dir = os.getcwd()
root_dir = f'{current_dir}/eyes_dataset'

train_dataset = CustomDataset(root_dir, transform=transform)
train_loader = DataLoader(dataset=train_dataset, batch_size=1, shuffle=True)

total_training_examples = 14 * 20
batch_size = 1
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)


# Initialize the model
model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)

# Update the number of classes in the classifier
num_classes = 14
num_ftrs = model.classifier[-1].in_features
model.classifier[-1] = nn.Linear(num_ftrs, 14)

# Move model to GPU if available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Define the checkpoint file path
checkpoint_dir = os.getcwd()
checkpoint_path = os.path.join(checkpoint_dir, 'model_checkpoint.pth')

# Load saved checkpoints
if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch'] + 1
else:
    start_epoch = 0

# Training loop
num_epochs = 10
for epoch in range(start_epoch, num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f'Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}')
    torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    }, checkpoint_path)

# Prediction generation after training
model.eval()  # Set the model to evaluation mode
top1_predictions = []
top5_predictions = []

with torch.no_grad():
    for images in test_loader:
        images = images.to(device)
        outputs = model(images)

        # Top-1 predictions
        _, top1_pred = outputs.topk(1, 1, True, True)
        top1_predictions.extend(top1_pred.t().tolist()[0])

        # Top-5 predictions
        _, top5_pred = outputs.topk(5, 1, True, True)
        top5_predictions.extend(top5_pred.t().tolist())

# Save the top-1 predictions
with open('top1_predictions.txt', 'w') as f:
    for pred in top1_predictions:
        f.write(f'{pred}\n')

# Save the top-5 predictions
with open('top5_predictions.txt', 'w') as f:
    for preds in top5_predictions:
        f.write(' '.join(map(str, preds)) + '\n')
