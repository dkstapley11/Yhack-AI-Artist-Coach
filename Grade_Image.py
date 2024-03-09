import torch
from torchvision import transforms, models
from torchvision.models.efficientnet import EfficientNet_B0_Weights
import torch.nn as nn
import os
from PIL import Image
from load_classes import main
import argparse

transform = transforms.Compose([
    lambda x: x.convert("RGB"),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

class_names = main()

def predict_image(input_image_path, ground_truth_class=None):
    # Initialize the model
    model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
    num_ftrs = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(num_ftrs, 14)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    checkpoint_path = 'model_state.pth'
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    image = Image.open(input_image_path)
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        sorted_probs, sorted_indices = torch.sort(probabilities, descending=True)

    top_class_idx = sorted_indices[0].item()
    top_class_name = class_names[top_class_idx]
    top_class_prob = sorted_probs[0].item()

    print(f"{top_class_name} is the most likely class for the input image.")

    if ground_truth_class is not None:
        ground_truth_idx = class_names.index(ground_truth_class)
        ground_truth_prob = probabilities[ground_truth_idx].item()
        print(f"Accuracy for the ground truth class '{ground_truth_class}': {ground_truth_prob * 100:.2f}%")

    for idx, prob in zip(sorted_indices, sorted_probs):
        class_idx = idx.item()
        class_name = class_names[class_idx]
        confidence = prob.item() * 100.0  # Convert to percentage

        # Check if this class is the ground truth
        is_ground_truth = class_idx == ground_truth_idx if ground_truth_class is not None else False
        ground_truth_marker = "(Ground Truth)" if is_ground_truth else ""

        print(f"Class: {class_name} - Confidence: {confidence:.2f}% {ground_truth_marker}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_image_path', type=str, help='Path to the input image')
    parser.add_argument('--ground_truth', type=str, default=None, help='Ground truth class (optional)')
    args = parser.parse_args()

    predict_image(args.input_image_path, args.ground_truth)