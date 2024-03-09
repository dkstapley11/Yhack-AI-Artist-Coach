import torch
from torchvision import transforms, models
from torchvision.models.efficientnet import EfficientNet_B0_Weights
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
import os
from PIL import Image
import yaml


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

image_path = f'{os.getcwd()}/output.png'



def main():
    

    predictions = []  # A list to hold path and predictions

    # Initialize the model
    model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
    

    num_ftrs = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(num_ftrs, 14)

    # Move model to GPU if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    checkpoint_path = 'model_state.pth'
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model.load_state_dict(checkpoint['model_state_dict'])

    with torch.no_grad():
        image_path = image_path.to(device)
        output = model(image_path)



    # with torch.no_grad():
    #     for images, paths in test_loader:
    #         images = images.to(device)
    #         outputs = model(images)

    #         _, top1_pred = outputs.topk(1, 1, True, True)
    #         _, top5_pred = outputs.topk(5, 1, True, True)
            
    #         top1_pred = top1_pred.squeeze().tolist()
    #         top5_pred = top5_pred.tolist()
            

if __name__ == '__main__':
    main()