# 🌿 Cassava Disease Detection System

An AI-powered application for detecting cassava leaf diseases with automatic validation and comprehensive PDF report generation for farmers.

## ✨ Key Features

- **Multi-Transform Fusion Model**: Uses DCT, STFT, Wavelet, and learnable transforms
- **Dual Backbone Architecture**: Combines MobileNetV2 and ConvNeXt-Tiny
- **Cassava Leaf Validation**: Automatically detects if uploaded image is a cassava leaf
- **PDF Report Generation**: Creates detailed farmer-friendly disease reports
- **5 Disease Classes**: CBB, CBSD, CGM, CMD, and Healthy
- **Real-time Predictions**: Fast inference with confidence scores
- **User-Friendly Interface**: Modern React frontend with drag-and-drop

## 🚀 Quick Start

### Windows Users

1. **Install Dependencies**:
   ```bash
   INSTALL.bat
   ```

2. **Start Application**:
   ```bash
   START_APP.bat
   ```

3. **Open Browser**: Navigate to `http://localhost:3000`

### Manual Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## 📋 Requirements

- Python 3.8+
- Node.js 14+
- 4GB RAM minimum
- Model weights file: `FusionNet/fusionnet_best.pth`

## 🎯 Usage

1. **Upload Image**: Drag and drop or click to upload a cassava leaf image
2. **Analyze**: Click "Analyze Image" to detect diseases
3. **Generate Report**: Click "Generate Report" to download a comprehensive PDF

### What's in the PDF Report?

- Disease detection analysis
- Scientific cause and summary
- Symptoms at all stages
- Recommended medicines with dosages
- Prevention methods
- 7-day treatment schedule
- Farmer-friendly recommendations

## 🏗️ Architecture

```
Frontend (React) → Backend (FastAPI) → AI Model (PyTorch)
                                    ↓
                            Cassava Validator
                                    ↓
                            PDF Generator
```

## 📁 Project Structure

```
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── models.py        # Neural network
│   ├── cassava_validator.py  # Leaf validation
│   ├── pdf_generator.py      # Report generation
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   └── components/
│   └── package.json
├── FusionNet/          # Model weights
├── SETUP_GUIDE.md      # Detailed setup instructions
├── INSTALL.bat         # Windows installation script
└── START_APP.bat       # Windows startup script
```

## 🔧 API Endpoints

- `POST /predict` - Detect disease from image
- `POST /generate-report` - Generate PDF report
- `GET /health` - Health check
- `GET /model-info` - Model information
- `GET /docs` - Interactive API documentation

## 🌐 Supported Diseases

1. **Cassava Bacterial Blight (CBB)** - Bacterial infection causing wilting
2. **Cassava Brown Streak Disease (CBSD)** - Viral disease with stem streaks
3. **Cassava Green Mottle (CGM)** - Viral disease with mottling patterns
4. **Cassava Mosaic Disease (CMD)** - Most common viral disease
5. **Healthy** - No disease detected

## 🛠️ Technology Stack

### Backend
- FastAPI - Modern Python web framework
- PyTorch - Deep learning framework
- ReportLab - PDF generation
- OpenCV - Image processing
- PyWavelets - Wavelet transforms

### Frontend
- React - UI framework
- Axios - HTTP client
- Lucide React - Icons
- React Router - Navigation

## 📊 Model Performance

- **Architecture**: MidFusionNet (8-branch fusion)
- **Input Size**: 224x224
- **Transforms**: 4 types (DCT, STFT, Wavelet, Learnable)
- **Backbones**: 2 (MobileNetV2, ConvNeXt-Tiny)
- **Classes**: 5

## 🐛 Troubleshooting

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting steps.

Common issues:
- **Module not found**: Run `pip install -r backend/requirements.txt`
- **Port in use**: Change port or kill existing process
- **Model not found**: Ensure `fusionnet_best.pth` exists in `FusionNet/`

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For issues and questions, please check the SETUP_GUIDE.md or create an issue in the repository.

---

**Made with ❤️ for farmers and agricultural researchers**
