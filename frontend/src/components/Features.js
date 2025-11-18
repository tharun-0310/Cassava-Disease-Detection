import React from 'react';
import { Brain, Zap, Shield, Target } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: <Brain size={32} />,
      title: "Multi-Transform Fusion",
      description: "Advanced neural network combining DCT, STFT, Wavelet, and learnable transforms for comprehensive image analysis."
    },
    {
      icon: <Zap size={32} />,
      title: "Dual Backbone Architecture",
      description: "Leverages both MobileNetV2 and ConvNeXt-Tiny models for optimal performance and accuracy."
    },
    {
      icon: <Target size={32} />,
      title: "High Accuracy Detection",
      description: "Identifies 5 different cassava conditions including CBB, CBSD, CGM, CMD, and healthy plants."
    },
    {
      icon: <Shield size={32} />,
      title: "Reliable & Fast",
      description: "Real-time processing with confidence scores to help farmers make informed decisions quickly."
    }
  ];

  return (
    <section id="features" className="features">
      <div className="container">
        <h2>Why Choose CassavaAI?</h2>
        <div className="grid grid-2">
          {features.map((feature, index) => (
            <div key={index} className="card feature-card">
              <div className="feature-icon">
                {feature.icon}
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;