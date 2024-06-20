import React, { useState, useEffect } from 'react';
import './JsonOut.css';
import photo1Path from './Run2012B_DoubleElectron_FourElectrons_Higgs_mass.png';
import photo2Path from './Run2012B_DoubleElectron_FourElectrons_Z1_mass.png';
import photo3Path from './Run2012B_DoubleElectron_FourElectrons_Z2_mass.png';
import photo4Path from './Run2012B_DoubleElectron_TwoMuonsTwoElectrons_Higgs_mass.png';
import photo5Path from './Run2012B_DoubleElectron_TwoMuonsTwoElectrons_Z1_mass.png';
import photo6Path from './Run2012B_DoubleElectron_TwoMuonsTwoElectrons_Z2_mass.png';


function JsonOut({ optionData, image1Data, image2Data, image3Data, image4Data, image5Data, image6Data }) {
  const [option, setOption] = useState(null);
  const [photo1, setPhoto1] = useState(null);
  const [photo2, setPhoto2] = useState(null);
  const [photo3, setPhoto3] = useState(null);
  const [photo4, setPhoto4] = useState(null);
  const [photo5, setPhoto5] = useState(null);
  const [photo6, setPhoto6] = useState(null);

  useEffect(() => {
    if (option !== null) {
      // Guardar las rutas de las fotos en los estados correspondientes
      setPhoto1(photo1Path);
      setPhoto2(photo2Path);
      setPhoto3(photo3Path);
      setPhoto4(photo4Path);
      setPhoto5(photo5Path);
      setPhoto6(photo6Path);
    }
  }, [option]);

  useEffect(() => {
    setOption(optionData);
  }, [optionData]);

  return (
    <div className='row'>
      <div className="col-lg-6">
        <div className="halfBoxImage2">
          <div className="titulo">Obtenidos por filtrado</div>
          <div className='head'>FourElectrons</div>
          <div className='row'>
            <div className="nombre">Higgs Mass</div>
            <div className="nombre">Z1 Mass</div>
            <div className="nombre">Z2 Mass</div>
          </div>
          <div className="row">
            <div className="halfBoxImage1">{photo1 ? (
              <img src={photo1} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p className='textosalida'>...</p>
            )}</div>
            <div className="halfBoxImage1">{photo2 ? (
              <img src={photo2} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p className='textosalida'>...</p>
            )}</div>
            <div className="halfBoxImage1">{photo3 ? (
              <img src={photo3} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p className='textosalida'>...</p>
            )}</div>
          </div>
          <div className='footer'>TwoMuonsTwoElectrons</div>
          <div className='row'>
            <div className="nombre">Higgs Mass</div>
            <div className="nombre">Z1 Mass</div>
            <div className="nombre">Z2 Mass</div>
          </div>
          <div className='row'>
            <div className="halfBoxImage1">{photo4 ? (
              <img src={photo4} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p className='textosalida'>...</p>
            )}</div>
            <div className="halfBoxImage1">{photo5 ? (
              <img src={photo5} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p className='textosalida'>...</p>
            )}</div>
            <div className="halfBoxImage1">{photo6 ? (
              <img src={photo6} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p className='textosalida'>...</p>
            )}</div>
          </div>
        </div>
      </div>
      <div className="halfBoxImage2">
        <div className="titulo">Obtenidos por Árbol de Decisión</div>
        <div className='head'>FourElectrons</div>
        <div className='row'>
          <div className="nombre">Higgs Mass</div>
          <div className="nombre">Z1 Mass</div>
          <div className="nombre">Z2 Mass</div>
        </div>
        <div className="row">
          <div className="halfBoxImage1">{image1Data ? (
            <img src={image1Data} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <p className='textosalida'>...</p>
          )}</div>
          <div className="halfBoxImage1">{image2Data ? (
            <img src={image2Data} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <p className='textosalida'>...</p>
          )}</div>
          <div className="halfBoxImage1">{image3Data ? (
            <img src={image3Data} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <p className='textosalida'>...</p>
          )}</div>
        </div>
        <div className='footer'>TwoMuonsTwoElectrons</div>
        <div className='row'>
          <div className="nombre">Higgs Mass</div>
          <div className="nombre">Z1 Mass</div>
          <div className="nombre">Z2 Mass</div>
        </div>
        <div className='row'>
          <div className="halfBoxImage1">{image4Data ? (
            <img src={image4Data} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <p className='textosalida'>...</p>
          )}</div>
          <div className="halfBoxImage1">{image5Data ? (
            <img src={image5Data} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <p className='textosalida'>...</p>
          )}</div>
          <div className="halfBoxImage1">{image6Data ? (
            <img src={image6Data} alt="Imagen" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <p className='textosalida'>...</p>
          )}</div>
        </div>
      </div>
    </div>
  );

}
export default JsonOut;

