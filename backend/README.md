# Fusion Model API

FastAPI backend for the Multi-Transform Fusion Model for Cassava Disease Classification.

## Features

- **Multi-Transform Processing**: DCT, STFT, Wavelet, and Learnable transforms
- **Dual Backbone Architecture**: MobileNetV2 + ConvNeXt-Tiny
- **REST API**: Simple POST endpoint for image classification
- **Cassava Leaf Validation**: Automatically detects if uploaded image is a cassava leaf
- **PDF Report Generation**: Creates comprehensive farmer-friendly disease reports
- **Automatic Model Loading**: Loads pre-trained weights on startup
- **Input Validation**: File type and size validation
- **CORS Support**: Cross-origin requests enabled

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Model Weights Exist**:
   - Place your trained model weights at: `../FusionNet/fusionnet_best.pth`
   - Or update the `MODEL_PATH` in `config.py`

3. **Run the API**:
   ```bash
   python run.py
   ```
   
   Or directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### POST /predict
Upload an image for classification.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file (jpg, jpeg, png, bmp, tiff)
- Max file size: 10MB

**Response (Success)**:
```json
{
  "predicted_class": "Healthy",
  "predicted_class_id": 4,
  "confidence": 0.8945,
  "is_cassava_leaf": true,
  "cassava_confidence": 0.87,
  "all_probabilities": {
    "Cassava Bacterial Blight (CBB)": 0.0123,
    "Cassava Brown Streak Disease (CBSD)": 0.0234,
    "Cassava Green Mottle (CGM)": 0.0345,
    "Cassava Mosaic Disease (CMD)": 0.0353,
    "Healthy": 0.8945
  },
  "filename": "test_image.jpg",
  "image_size": [640, 480],
  "image_mode": "RGB"
}
```

**Response (Not Cassava Leaf)**:
```json
{
  "error": "Not a cassava leaf",
  "message": "The uploaded image does not appear to be a cassava leaf...",
  "is_cassava_leaf": false,
  "cassava_confidence": 0.32,
  "filename": "test_image.jpg"
}
```

### POST /generate-report
Generate a comprehensive PDF report for the detected disease.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file (jpg, jpeg, png, bmp, tiff)
- Max file size: 10MB

**Response**:
- Returns a PDF file download with comprehensive disease information including:
  - Disease analysis and detection explanation
  - Disease summary and scientific cause
  - Symptoms at different stages
  - Recommended medicines with dosages
  - Prevention methods
  - 7-day treatment schedule
  - Final recommendations for farmers

### GET /health
Health check endpoint.

### GET /model-info
Get model information and configuration.

### GET /
Root endpoint with basic API information.

## Usage Example

### Python
```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("cassava_leaf.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(f"Prediction: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.4f}")
```

### cURL
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@cassava_leaf.jpg"
```

## Configuration

Edit `config.py` to modify:
- Model path and parameters
- API settings (max file size, allowed extensions)
- Class names
- Device selection (CPU/CUDA)

## Model Architecture

The API uses a Multi-Transform Fusion Network with:
- **4 Transform Types**: DCT, STFT, Wavelet, Learnable
- **2 Backbones**: MobileNetV2 and ConvNeXt-Tiny  
- **8 Branches**: Each transform processed by both backbones
- **Mid-Level Fusion**: Features combined before final classification

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.