from torchvision import transforms
import os
from torchvision.datasets import ImageFolder


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

class CustomDataset(ImageFolder):
    def __init__(self, root, transform=None):
        super().__init__(root, transform=transform)
        

def main():
    current_dir = os.getcwd()
    root_dir = f'{current_dir}/eyes_dataset'
    dataset = CustomDataset(root_dir, transform=transform)
    
    # Extract class names
    class_names = dataset.classes
    print(class_names)
    return class_names

if __name__ == "__main__":
    main()