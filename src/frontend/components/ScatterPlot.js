import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { getScatterPlot } from '../services/api';

const ScatterPlot = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getScatterPlot().then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <Plot
      data={JSON.parse(data).data}
      layout={JSON.parse(data).layout}
    />
  );
};

export default ScatterPlot;
