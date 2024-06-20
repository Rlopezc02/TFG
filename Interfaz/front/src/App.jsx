import React, { useState, useEffect, useCallback } from 'react';
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css';
import Botones from './components/Botones.jsx';
import JsonOut from './components/JsonOut.jsx';

function App() {
  const [optionData, setOptionData] = useState(null);
  const [image1Data, setImage1Data] = useState(null);
  const [image2Data, setImage2Data] = useState(null);
  const [image3Data, setImage3Data] = useState(null);
  const [image4Data, setImage4Data] = useState(null);
  const [image5Data, setImage5Data] = useState(null);
  const [image6Data, setImage6Data] = useState(null);

  const handleOptionReceived = (option) => {
    setOptionData(option);
  };

  const handleImage1Received = (image1) => {
    setImage1Data(image1);
  };
  const handleImage2Received = (image2) => {
    setImage2Data(image2);
  };
  const handleImage3Received = (image3) => {
    setImage3Data(image3);
  };
  const handleImage4Received = (image4) => {
    setImage4Data(image4);
  };
  const handleImage5Received = (image5) => {
    setImage5Data(image5);
  };
  const handleImage6Received = (image6) => {
    setImage6Data(image6);
  };


 
  return (
    <div className="container">
      <Botones onOptionReceived={handleOptionReceived} onImage1Received={handleImage1Received} onImage2Received={handleImage2Received} onImage3Received={handleImage3Received} onImage4Received={handleImage4Received} onImage5Received={handleImage5Received} onImage6Received={handleImage6Received}/>
      <JsonOut optionData={optionData} image1Data={image1Data} image2Data={image2Data} image3Data={image3Data} image4Data={image4Data} image5Data={image5Data} image6Data={image6Data} />
    </div>     
    
  );
}

export default App;
