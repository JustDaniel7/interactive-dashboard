import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { getPriceDistribution } from '../services/api';

const PriceDistribution = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getPriceDistribution().then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <Plot
      data={JSON.parse(data).data}
      layout={JSON.parse(data).layout}
    />
  );
};

export default PriceDistribution;
