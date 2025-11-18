import io
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Dict, Any
from config import MODEL_CONFIG, MODEL_PATH, CLASS_NAMES
from models import MidFusionNet
from transforms import get_transforms


class ModelPredictor:
    def __init__(self):
        self.device = torch.device(MODEL_CONFIG["device"])
        self.model = None
        self.transforms = get_transforms()
        self.class_names = CLASS_NAMES
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            self.model = MidFusionNet(
                num_classes=MODEL_CONFIG["num_classes"],
                dropout=MODEL_CONFIG["dropout"]
            ).to(self.device)
            
            if MODEL_PATH.exists():
                state_dict = torch.load(MODEL_PATH, map_location=self.device)
                self.model.load_state_dict(state_dict)
                self.model.eval()
                print(f"Model loaded successfully from {MODEL_PATH}")
            else:
                print(f"Warning: Model file not found at {MODEL_PATH}")
                print("Model initialized with random weights")
                
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> Dict[str, torch.Tensor]:
        """Apply all transforms to the input image"""
        try:
            # Ensure image is RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Apply all transforms
            transformed_inputs = {}
            for name, transform in self.transforms.items():
                if name == "learn":
                    # Learnable transform needs special handling
                    transformed_inputs[name] = transform(image).unsqueeze(0).to(self.device)
                else:
                    transformed_inputs[name] = transform(image).unsqueeze(0).to(self.device)
            
            return transformed_inputs
            
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            raise
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Make prediction on input image"""
        try:
            # Preprocess image
            inputs = self.preprocess_image(image)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(inputs)
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
            
            # Prepare response
            result = {
                "predicted_class": self.class_names[predicted_class],
                "predicted_class_id": predicted_class,
                "confidence": float(confidence),
                "all_probabilities": {
                    self.class_names[i]: float(prob) 
                    for i, prob in enumerate(probabilities[0])
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            raise


def validate_image_file(file_content: bytes, filename: str) -> bool:
    """Validate if the uploaded file is a valid image"""
    try:
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        from config import API_CONFIG
        if file_ext not in API_CONFIG["allowed_extensions"]:
            return False
        
        # Try to open as image
        Image.open(io.BytesIO(file_content))
        return True
        
    except Exception:
        return False


# Global predictor instance
predictor = None

def get_predictor():
    """Get or create predictor instance"""
    global predictor
    if predictor is None:
        predictor = ModelPredictor()
    return predictor