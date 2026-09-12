from fastapi import FastAPI, UploadFile, File
from test import load_trained_model, get_transforms
import torch
import io
from PIL import Image
import os
import uvicorn
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Cyclone_resnet18_best.pth"

model, class_names, device = load_trained_model(str(MODEL_PATH))

# Load model once at server startup
model, class_names, device = load_trained_model("Cyclone_resnet18_best.pth")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    transform = get_transforms()
    input_tensor = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
    predicted_idx = torch.argmax(probabilities).item()
    
    return {
        "filename": file.filename,
        "prediction": class_names[predicted_idx],
        "confidence": float(probabilities[predicted_idx])
    }
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
