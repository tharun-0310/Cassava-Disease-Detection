import io
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image
from typing import Dict, Any
from pathlib import Path

from config import API_CONFIG
from utils import get_predictor, validate_image_file
from cassava_validator import get_validator
from pdf_generator import get_pdf_generator

# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the model predictor on startup"""
    try:
        get_predictor()
        print("Model predictor initialized successfully")
    except Exception as e:
        print(f"Failed to initialize model predictor: {e}")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Fusion Model API is running",
        "version": API_CONFIG["version"],
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        predictor = get_predictor()
        return {
            "status": "healthy",
            "model_loaded": predictor.model is not None,
            "device": str(predictor.device),
            "num_classes": len(predictor.class_names)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Predict the class of an uploaded image using the fusion model
    
    Args:
        file: Uploaded image file (jpg, jpeg, png, bmp, tiff)
    
    Returns:
        Dictionary containing prediction results
    """
    try:
        # Validate file size
        file_content = await file.read()
        if len(file_content) > API_CONFIG["max_file_size"]:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {API_CONFIG['max_file_size']} bytes"
            )
        
        # Validate file type
        if not validate_image_file(file_content, file.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid image file. Supported formats: jpg, jpeg, png, bmp, tiff"
            )
        
        # Load image
        try:
            image = Image.open(io.BytesIO(file_content))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not process image: {str(e)}"
            )
        
        # FEATURE 1: Validate if image is a cassava leaf
        validator = get_validator()
        is_cassava, cassava_confidence, validation_message = validator.validate(image)
        
        if not is_cassava:
            return {
                "error": "Not a cassava leaf",
                "message": "The uploaded image does not appear to be a cassava leaf. Please upload a clear image of a cassava leaf for disease detection.",
                "is_cassava_leaf": False,
                "cassava_confidence": float(cassava_confidence),
                "filename": file.filename
            }
        
        # Get predictor and make prediction
        predictor = get_predictor()
        result = predictor.predict(image)
        
        # Add metadata
        result["filename"] = file.filename
        result["image_size"] = image.size
        result["image_mode"] = image.mode
        result["is_cassava_leaf"] = True
        result["cassava_confidence"] = float(cassava_confidence)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/generate-report")
async def generate_report(file: UploadFile = File(...)):
    """
    Generate comprehensive PDF report for detected disease
    
    Args:
        file: Uploaded image file
    
    Returns:
        PDF file download
    """
    try:
        # Validate and process image (same as predict endpoint)
        file_content = await file.read()
        if len(file_content) > API_CONFIG["max_file_size"]:
            raise HTTPException(status_code=413, detail="File too large")
        
        if not validate_image_file(file_content, file.filename):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        image = Image.open(io.BytesIO(file_content))
        
        # Validate cassava leaf
        validator = get_validator()
        is_cassava, cassava_confidence, validation_message = validator.validate(image)
        
        if not is_cassava:
            raise HTTPException(
                status_code=400,
                detail="Not a cassava leaf. Cannot generate report for non-cassava images."
            )
        
        # Get prediction
        predictor = get_predictor()
        result = predictor.predict(image)
        
        # FEATURE 2: Generate PDF report
        pdf_generator = get_pdf_generator()
        pdf_path = pdf_generator.generate_report(result)
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=Path(pdf_path).name,
            headers={"Content-Disposition": f"attachment; filename={Path(pdf_path).name}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )


@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    try:
        predictor = get_predictor()
        return {
            "model_type": "MidFusionNet",
            "num_classes": len(predictor.class_names),
            "class_names": predictor.class_names,
            "device": str(predictor.device),
            "transforms": list(predictor.transforms.keys()),
            "input_size": [224, 224],
            "model_loaded": predictor.model is not None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting model info: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )