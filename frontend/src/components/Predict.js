import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, Image as ImageIcon, Loader, AlertCircle, FileText, Download } from 'lucide-react';

const Predict = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [generatingPDF, setGeneratingPDF] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setError(null);
      setPrediction(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(file);
    } else {
      setError('Please select a valid image file (JPG, PNG, BMP, TIFF)');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Check if it's a cassava leaf
      if (response.data.is_cassava_leaf === false) {
        setError(response.data.message || 'This does not appear to be a cassava leaf image.');
        setPrediction(null);
      } else {
        setPrediction(response.data);
      }
    } catch (err) {
      console.error('Prediction error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to get prediction. Please make sure the backend server is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setGeneratingPDF(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/generate-report', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob', // Important for file download
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from response headers or use default
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'Cassava_Disease_Report.pdf';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error('PDF generation error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to generate PDF report. Please try again.'
      );
    } finally {
      setGeneratingPDF(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setPreview(null);
    setPrediction(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getHealthStatus = (className) => {
    return className === 'Healthy' ? 'healthy' : 'diseased';
  };

  const formatConfidence = (confidence) => {
    return (confidence * 100).toFixed(1);
  };

  return (
    <section className="predict-section">
      <div className="container">
        <div className="predict-container">
          <h1 className="predict-title">Cassava Disease Detection</h1>
          
          <div className="card">
            <div 
              className={`upload-area ${dragOver ? 'dragover' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={handleUploadClick}
            >
              <div className="upload-icon">
                {preview ? <ImageIcon size={64} /> : <Upload size={64} />}
              </div>
              
              {preview ? (
                <div>
                  <img src={preview} alt="Preview" className="image-preview" />
                  <p className="upload-text">Image selected: {selectedFile?.name}</p>
                  <p className="upload-subtext">Click to change image or drag & drop a new one</p>
                </div>
              ) : (
                <div>
                  <p className="upload-text">Click to upload or drag & drop</p>
                  <p className="upload-subtext">
                    Supports JPG, PNG, BMP, TIFF (max 10MB)
                  </p>
                </div>
              )}
              
              <input
                ref={fileInputRef}
                type="file"
                className="file-input"
                accept="image/*"
                onChange={handleFileChange}
              />
            </div>

            {error && (
              <div className="error">
                <AlertCircle size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                {error}
              </div>
            )}

            <div className="text-center">
              <button 
                className="btn btn-primary"
                onClick={handlePredict}
                disabled={!selectedFile || loading || generatingPDF}
                style={{ marginRight: '12px' }}
              >
                {loading ? (
                  <>
                    <Loader size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                    Analyzing...
                  </>
                ) : (
                  'Analyze Image'
                )}
              </button>
              
              {prediction && prediction.is_cassava_leaf && (
                <button 
                  className="btn btn-success"
                  onClick={handleGeneratePDF}
                  disabled={loading || generatingPDF}
                  style={{ marginRight: '12px' }}
                >
                  {generatingPDF ? (
                    <>
                      <Loader size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                      Generating PDF...
                    </>
                  ) : (
                    <>
                      <FileText size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                      Generate Report
                    </>
                  )}
                </button>
              )}
              
              {(selectedFile || prediction) && (
                <button 
                  className="btn btn-secondary"
                  onClick={resetForm}
                  disabled={loading || generatingPDF}
                >
                  Reset
                </button>
              )}
            </div>
          </div>

          {loading && (
            <div className="loading">
              <Loader size={48} />
              <p>Processing image with multi-transform fusion model...</p>
            </div>
          )}

          {prediction && (
            <div className="prediction-result">
              <h3 className="result-title">Detection Results</h3>
              
              <div className="result-main">
                <div>
                  <div className="result-class">{prediction.predicted_class}</div>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill"
                      style={{ width: `${formatConfidence(prediction.confidence)}%` }}
                    ></div>
                  </div>
                </div>
                <div className="result-confidence">
                  {formatConfidence(prediction.confidence)}% confident
                </div>
              </div>

              <div className="all-probabilities">
                <h4 style={{ marginBottom: '16px', color: '#333' }}>All Predictions:</h4>
                {Object.entries(prediction.all_probabilities).map(([className, probability]) => (
                  <div key={className} className="probability-item">
                    <span className="probability-name">{className}</span>
                    <span className="probability-value">{formatConfidence(probability)}%</span>
                  </div>
                ))}
              </div>

              <div style={{ marginTop: '20px', padding: '16px', background: '#f8f9fa', borderRadius: '8px' }}>
                <p style={{ margin: '0', color: '#666', fontSize: '0.9rem' }}>
                  <strong>Image:</strong> {prediction.filename} | 
                  <strong> Size:</strong> {prediction.image_size?.[0]}×{prediction.image_size?.[1]} | 
                  <strong> Mode:</strong> {prediction.image_mode}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default Predict;