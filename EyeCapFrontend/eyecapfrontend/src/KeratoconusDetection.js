import React, { useState } from 'react';

function KeratoconusDetection() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState('');
  const [probability, setProbability] = useState(0);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      alert('Please select an image.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch('/predict_keratoconus', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setPrediction(data.prediction);
        setProbability(data.probability);
      } else {
        const errorData = await response.json();
        console.error('Error Response:', errorData);
        alert('Error while making the prediction.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error occurred while making the prediction.');
    }
  };

  return (
    <div>
      <h1>Keratoconus Detection</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      <button onClick={handlePredict}>Predict</button>
      {selectedImage && <img src={URL.createObjectURL(selectedImage)} alt="Selected" />}
      {prediction && (
        <div>
          <h2>Prediction: {prediction}</h2>
          <p>Probability: {probability}</p>
        </div>
      )}
    </div>
  );
}

export default KeratoconusDetection;
