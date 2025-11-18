import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Scan } from 'lucide-react';

const Hero = () => {
  return (
    <section className="hero">
      <div className="container">
        <h1>Cassava Disease Detection</h1>
        <p>
          Advanced AI-powered detection system using multi-transform fusion networks 
          to identify cassava plant diseases with high accuracy. Protect your crops 
          with cutting-edge machine learning technology.
        </p>
        <div className="hero-buttons">
          <Link to="/predict" className="btn btn-primary">
            <Scan size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            Start Detection
            <ArrowRight size={20} style={{ marginLeft: '8px', verticalAlign: 'middle' }} />
          </Link>
          <a href="#features" className="btn btn-secondary">
            Learn More
          </a>
        </div>
      </div>
    </section>
  );
};

export default Hero;