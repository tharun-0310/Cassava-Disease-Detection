import os 
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)
MODEL_PATH = BASE_DIR / "Final_pipeline"/"fusionnet_best.pth"
print(MODEL_PATH)

# Model configuration
MODEL_CONFIG = {
    "num_classes": 5,
    "dropout": 0.4,
    "device": "cuda" if os.environ.get("CUDA_AVAILABLE") == "true" else "cpu"
}

# API configuration
API_CONFIG = {
    "title": "Fusion Model API",
    "description": "Multi-transform fusion model for image classification",
    "version": "1.0.0",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "allowed_extensions": {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
}

# Class names from dataset
CLASS_NAMES = [
    "Cassava Bacterial Blight (CBB)",
    "Cassava Brown Streak Disease (CBSD)", 
    "Cassava Green Mottle (CGM)",
    "Cassava Mosaic Disease (CMD)",
    "Healthy"
]