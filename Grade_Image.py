import torch
from torchvision import transforms, models
from torchvision.models.efficientnet import EfficientNet_B0_Weights
import torch.nn as nn
import os
from PIL import Image
from load_classes import main


transform = transforms.Compose([
    lambda x: x.convert("RGB"),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

class_names = main()

image_path = f'{os.getcwd()}/output.png'


def main():
    

    predictions = []  # A list to hold path and predictions

    # Initialize the model
    model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    image_path = f'{os.getcwd()}/output.png'
    image = Image.open(image_path)
    image_tensor = transform(image).unsqueeze(0).to(device)
    

    num_ftrs = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(num_ftrs, 14)

    # Move model to GPU if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    checkpoint_path = 'model_state.pth'
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model.load_state_dict(checkpoint['model_state_dict'])

    model.eval()

    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        sorted_probs, sorted_indices = torch.sort(probabilities, descending=True)
    
    top_class_idx = sorted_indices[0].item()
    top_class_name = class_names[top_class_idx]
    top_class_prob = sorted_probs[0].item()

    ground_truth_idx = 5
    ground_truth_name = class_names[ground_truth_idx]

    accuracy = 100.0 * top_class_prob if top_class_idx == ground_truth_idx else 0.0

    print(f"{top_class_name} is the most likely class for what you drew!")
    print(f"You were {accuracy:.2f}% accurate compared to the ground truth class {ground_truth_name}.")

            

if __name__ == '__main__':
    main()