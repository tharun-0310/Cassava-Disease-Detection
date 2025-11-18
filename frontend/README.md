# Cassava Disease Detection Frontend

React frontend for the Multi-Transform Fusion Model API for cassava disease classification.

## Features

- **Modern React UI**: Clean, responsive design with smooth animations
- **Drag & Drop Upload**: Easy image upload with drag and drop support
- **Real-time Predictions**: Instant disease detection results
- **Detailed Results**: Shows confidence scores and all class probabilities
- **Mobile Responsive**: Works seamlessly on all devices
- **Error Handling**: Comprehensive error messages and validation

## Components

### Navbar
- Navigation between Home and Predict pages
- Responsive design with brand logo

### Hero Section
- Eye-catching landing section
- Call-to-action buttons
- Gradient background

### Features Section
- Highlights key capabilities
- Grid layout with icons
- Technical details about the model

### Predict Section
- Image upload interface
- Drag & drop functionality
- Real-time prediction results
- Confidence visualization
- Detailed probability breakdown

## Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/predict`.

### Prediction Flow:
1. User uploads image via drag & drop or file picker
2. Image is validated (type, size)
3. FormData is sent to `/predict` endpoint
4. Results are displayed with confidence scores
5. All class probabilities are shown

### Error Handling:
- File type validation
- File size limits (10MB)
- Network error handling
- Backend error messages

## Supported Image Formats

- JPG/JPEG
- PNG
- BMP
- TIFF
- Maximum size: 10MB

## Disease Classes

The model detects 5 cassava conditions:
1. **Cassava Bacterial Blight (CBB)**
2. **Cassava Brown Streak Disease (CBSD)**
3. **Cassava Green Mottle (CGM)**
4. **Cassava Mosaic Disease (CMD)**
5. **Healthy**

## Usage

1. Navigate to the Predict page
2. Upload a cassava leaf image
3. Click "Analyze Image"
4. View the detection results with confidence scores
5. See detailed probability breakdown for all classes

## Development

### Project Structure:
```
src/
├── components/
│   ├── Navbar.js       # Navigation component
│   ├── Home.js         # Home page wrapper
│   ├── Hero.js         # Hero section
│   ├── Features.js     # Features showcase
│   └── Predict.js      # Prediction interface
├── App.js              # Main app component
├── App.css             # Main styles
├── index.js            # React entry point
└── index.css           # Global styles
```

### Key Dependencies:
- **React Router**: Page navigation
- **Axios**: HTTP requests to backend
- **Lucide React**: Modern icons
- **React Scripts**: Development tools

## Customization

### Styling:
- Modify `App.css` for component styles
- Update `index.css` for global styles
- Colors and gradients can be customized

### API Endpoint:
- Update the API URL in `Predict.js` if backend runs on different port
- Proxy is configured in `package.json` for development

### Features:
- Add new disease classes by updating the display logic
- Extend with additional model information
- Add image preprocessing preview