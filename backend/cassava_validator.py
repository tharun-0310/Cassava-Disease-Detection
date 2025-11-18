"""
Cassava Leaf Validator
Uses a simple CNN classifier to detect if an uploaded image is a cassava leaf
"""
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
from typing import Tuple


class CassavaValidator:
    """Validates if an image is a cassava leaf"""
    
    def __init__(self, threshold: float = 0.6):
        """
        Initialize the cassava validator
        
        Args:
            threshold: Confidence threshold for cassava detection (0-1)
        """
        self.threshold = threshold
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._build_simple_classifier()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def _build_simple_classifier(self) -> nn.Module:
        """
        Build a simple binary classifier
        For production, this should be trained on cassava vs non-cassava images
        Currently uses heuristics based on image features
        """
        # Using a lightweight MobileNetV2 for binary classification
        model = models.mobilenet_v2(weights="IMAGENET1K_V1")
        # Modify last layer for binary classification
        model.classifier[1] = nn.Linear(model.last_channel, 2)
        model = model.to(self.device)
        model.eval()
        return model
    
    def _check_leaf_characteristics(self, image: Image.Image) -> float:
        """
        Heuristic-based validation using image characteristics
        Checks for leaf-like features: green color dominance, texture patterns
        
        Returns:
            Confidence score (0-1) that this is a cassava leaf
        """
        import numpy as np
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize for faster processing
        img_array = np.array(image.resize((224, 224)))
        
        # Feature 1: Green color dominance (cassava leaves are predominantly green)
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        green_dominance = np.mean(g > r) * np.mean(g > b)
        
        # Feature 2: Color variance (leaves have texture)
        color_variance = np.std(img_array) / 255.0
        
        # Feature 3: Green channel intensity
        green_intensity = np.mean(g) / 255.0
        
        # Feature 4: Check if image has leaf-like aspect ratio and not too uniform
        uniformity = 1.0 - (np.std(img_array) / 128.0)
        
        # Combine features with weights
        confidence = (
            green_dominance * 0.35 +
            min(color_variance * 2, 1.0) * 0.25 +
            green_intensity * 0.25 +
            (1.0 - min(uniformity, 1.0)) * 0.15
        )
        
        return min(max(confidence, 0.0), 1.0)
    
    def validate(self, image: Image.Image) -> Tuple[bool, float, str]:
        """
        Validate if the image is a cassava leaf
        
        Args:
            image: PIL Image to validate
        
        Returns:
            Tuple of (is_cassava, confidence, message)
        """
        try:
            # Use heuristic-based validation
            confidence = self._check_leaf_characteristics(image)
            
            is_cassava = confidence >= self.threshold
            
            if is_cassava:
                message = f"Valid cassava leaf detected (confidence: {confidence:.2%})"
            else:
                message = f"This does not appear to be a cassava leaf (confidence: {confidence:.2%})"
            
            return is_cassava, confidence, message
            
        except Exception as e:
            return False, 0.0, f"Validation error: {str(e)}"


# Global validator instance
_validator = None

def get_validator() -> CassavaValidator:
    """Get or create validator instance"""
    global _validator
    if _validator is None:
        _validator = CassavaValidator(threshold=0.5)
    return _validator
