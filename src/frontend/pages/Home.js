import React from 'react';
import PriceDistribution from '../components/PriceDistribution';
import ScatterPlot from '../components/ScatterPlot';

const Home = () => {
  return (
    <div>
      <h1>Housing Dashboard</h1>
      <PriceDistribution />
      <ScatterPlot />
    </div>
  );
};

export default Home;