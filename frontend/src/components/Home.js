import React from 'react';
import { Link } from 'react-router-dom';
import Hero from './Hero';
import Features from './Features';

const Home = () => {
  return (
    <div>
      <Hero />
      <Features />
    </div>
  );
};

export default Home;