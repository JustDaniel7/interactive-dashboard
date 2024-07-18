"use client";

import React from "react";
import Image from "next/image";

interface ImageWithFallbackProps {
  src: string;
  alt: string;
  width: number;
  height: number;
}

const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({ src, alt, width, height }) => {
  const [error, setError] = React.useState<boolean>(false);

  const handleError = () => {
    setError(true);
  };

  if (error) {
    return (
      <div className="bg-gray-200 flex items-center justify-center" style={{ width, height }}>
        <p className="text-gray-500">Image not found</p>
      </div>
    );
  }

  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      onError={handleError}
    />
  );
};

const Home: React.FC = () => {
  return (
    <div className="container mx-auto px-4">
      <main className="py-8">
        <h1 className="text-3xl font-bold mb-8 text-center">Visualizations from Python Notebook</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Visualization 1</h2>
            <ImageWithFallback src="/plot1.png" alt="Visualization 1" width={500} height={300} />
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Visualization 2</h2>
            <ImageWithFallback src="/plot2.png" alt="Visualization 2" width={500} height={300} />
          </div>
        </div>
      </main>

      <footer className="mt-8 text-center text-gray-600">
        <p>Footer content here</p>
      </footer>
    </div>
  );
};

export default Home;