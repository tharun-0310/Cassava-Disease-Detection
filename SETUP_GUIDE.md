# Cassava Disease Detection - Complete Setup Guide

## 🌿 Overview
This application uses AI to detect cassava leaf diseases and generate comprehensive PDF reports for farmers.

### New Features
1. **Cassava Leaf Validation** - Automatically detects if uploaded image is actually a cassava leaf
2. **PDF Report Generation** - Creates detailed farmer-friendly reports with treatment plans

---

## 📋 Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **pip** (comes with Python)
- **npm** (comes with Node.js)

### Check Installations
```bash
python --version
node --version
npm --version
```

---

## 🚀 Installation Steps

### Step 1: Install Backend Dependencies

Open terminal/command prompt in the project root directory:

```bash
cd backend
pip install -r requirements.txt
```

**Note**: If you get errors installing PyTorch, use the CPU version:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Step 2: Install Frontend Dependencies

Open a new terminal window:

```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

### Option 1: Run Both Servers (Recommended)

**Terminal 1 - Backend Server:**
```bash
cd backend
python run.py
```

You should see:
```
Starting Fusion Model API...
API will be available at: http://localhost:8000
API documentation at: http://localhost:8000/docs
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
npm start
```

The browser will automatically open at `http://localhost:3000`

### Option 2: Run Separately

**Backend only:**
```bash
cd backend
python run.py
```

**Frontend only:**
```bash
cd frontend
npm start
```

---

## 🎯 Using the Application

### 1. Analyze a Cassava Leaf

1. Navigate to the **Predict** page
2. Upload a cassava leaf image (drag & drop or click to browse)
3. Click **"Analyze Image"**
4. View the disease detection results

**If the image is not a cassava leaf:**
- You'll see an error message: "This does not appear to be a cassava leaf"
- Upload a different image

**If the image is a cassava leaf:**
- You'll see the disease prediction with confidence scores
- All disease probabilities will be displayed

### 2. Generate PDF Report

After successful disease detection:

1. Click the **"Generate Report"** button
2. A comprehensive PDF will be automatically downloaded
3. The PDF includes:
   - Disease analysis and how it was detected
   - Disease summary and scientific cause
   - Symptoms at early, mid, and advanced stages
   - Recommended medicines with dosages and safety notes
   - Prevention methods
   - Future avoidance strategies
   - 7-day treatment schedule
   - Final recommendations (DO's and DON'Ts)

---

## 📁 Project Structure

```
Capstone Prj/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Neural network models
│   ├── utils.py                # Prediction utilities
│   ├── transforms.py           # Image transformations
│   ├── config.py               # Configuration
│   ├── cassava_validator.py   # NEW: Leaf validation
│   ├── pdf_generator.py        # NEW: PDF report generation
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Startup script
│   └── reports/                # Generated PDF reports
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Predict.js      # Main prediction interface
│   │   │   ├── Home.js
│   │   │   ├── Hero.js
│   │   │   └── Features.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.css
│   └── package.json
└── FusionNet/
    └── fusionnet_best.pth      # Trained model weights
```

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'uvicorn'`
**Solution**: Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Problem**: `Model file not found`
**Solution**: Ensure `fusionnet_best.pth` exists in `FusionNet/` folder

**Problem**: PyTorch installation fails
**Solution**: Install CPU version
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**Problem**: `reportlab` not found
**Solution**: 
```bash
pip install reportlab
```

### Frontend Issues

**Problem**: `npm install` fails
**Solution**: Clear cache and retry
```bash
npm cache clean --force
npm install
```

**Problem**: Port 3000 already in use
**Solution**: Kill the process or use different port
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or set different port
set PORT=3001 && npm start
```

**Problem**: Cannot connect to backend
**Solution**: Ensure backend is running on port 8000

### PDF Generation Issues

**Problem**: PDF download fails
**Solution**: 
- Check backend logs for errors
- Ensure `reports/` directory exists in backend folder
- Verify `reportlab` is installed

---

## 🌐 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## 📊 Supported Disease Classes

1. **Cassava Bacterial Blight (CBB)**
2. **Cassava Brown Streak Disease (CBSD)**
3. **Cassava Green Mottle (CGM)**
4. **Cassava Mosaic Disease (CMD)**
5. **Healthy**

---

## 🎨 Features in Detail

### Cassava Leaf Validation
- Uses heuristic-based image analysis
- Checks for green color dominance
- Analyzes texture patterns
- Validates leaf-like characteristics
- Threshold: 50% confidence

### PDF Report Contents
- **Section 1**: Disease Analysis - How the model detected the disease
- **Section 2**: Disease Summary - Scientific cause and background
- **Section 3**: Symptoms & Identification - Early, mid, and advanced stages
- **Section 4**: Recommended Medicines - Detailed table with dosages
- **Section 5**: Prevention Methods - Practical farming guidelines
- **Section 6**: Future Avoidance - Long-term prevention strategies
- **Section 7**: Treatment Plan - 7-day schedule with daily actions
- **Section 8**: Final Recommendations - DO's and DON'Ts

---

## 💡 Tips

1. **Best Image Quality**: Use clear, well-lit photos of cassava leaves
2. **Image Format**: JPG, PNG, BMP, or TIFF (max 10MB)
3. **Leaf Position**: Capture the entire leaf with visible symptoms
4. **Background**: Plain background works best
5. **Lighting**: Natural daylight provides best results

---

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review backend logs in the terminal
3. Check browser console for frontend errors (F12)
4. Verify all dependencies are installed
5. Ensure model weights file exists

---

## 📝 Notes

- The cassava validator uses heuristic analysis (can be improved with a trained model)
- PDF reports are saved in `backend/reports/` directory
- Backend runs on port 8000, frontend on port 3000
- CORS is enabled for development (configure for production)
- Model requires significant memory for inference

---

## ✅ Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Model weights file exists (`FusionNet/fusionnet_best.pth`)
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Browser opened to http://localhost:3000

---

**Ready to detect cassava diseases! 🌿**
