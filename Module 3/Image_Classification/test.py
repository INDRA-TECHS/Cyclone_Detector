import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# 1. Define Model Architecture & Load State Dict
def load_trained_model(model_path):
    # Class mapping extracted from data.pkl
    class_names = [
        "Depression",
        "Deep Depression",
        "Cyclonic Storm",
        "Severe Cyclonic Storm",
        "Very Severe Cyclonic Storm",
        "Extremely Severe Cyclonic Storm"
    ]
    
    # Initialize base ResNet-18 architecture with 6 output classes
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(class_names))
    
    # Load state dictionary
    # Uses map_location to ensure compatibility regardless of CPU/GPU availability
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load(model_path, map_location=device)
    
    # If saved as a checkpoint dict vs raw state_dict
    if 'model_state_dict' in state_dict:
        model.load_state_dict(state_dict['model_state_dict'])
    else:
        model.load_state_dict(state_dict)
        
    model.to(device)
    model.eval()
    return model, class_names, device

# 2. Define Image Preprocessing
def get_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

# 3. Single Image Inference Function
def predict_cyclone(image_path, model, class_names, device):
    transform = get_transforms()
    
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
    predicted_idx = torch.argmax(probabilities).item()
    predicted_class = class_names[predicted_idx]
    confidence = probabilities[predicted_idx].item()
    
    print(f"Prediction for {os.path.basename(image_path)}:")
    print(f"  Class: {predicted_class}")
    print(f"  Confidence: {confidence * 100:.2f}%\n")
    
    return predicted_class, confidence

# Usage Example
if __name__ == "__main__":
    model_path = "cyclone_resnet18_best.pth"
    model, class_names, device = load_trained_model(model_path)
    
    # Replace with path to your test satellite image
    test_image_path = "Test_Cyclone_Image.jpeg" 
    
    if os.path.exists(test_image_path):
        predict_cyclone(test_image_path, model, class_names, device)
    else:
        print(f"Model loaded successfully. Add a test image at '{test_image_path}' to run inference.")