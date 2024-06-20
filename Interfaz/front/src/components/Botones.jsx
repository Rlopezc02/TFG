import React, { useRef, useState } from 'react';
import './Botones.css';
import '../App.css';
import '../App.jsx';
// import csv from './Run2012B_DoubleElectron.csv';


function Botones({ onOptionReceived,onImage1Received,onImage2Received,onImage3Received,onImage4Received,onImage5Received,onImage6Received}) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [messages, setMessages] = useState([])

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option) => {
    setSelectedOption(option);
    setIsOpen(false);
    onOptionReceived(option);
  };


  const options = [
    { value: 'option1', label: 'Run2012B_DoubleElectron' },
    { value: 'option2', label: 'Database 2' },
    { value: 'option3', label: 'Database 3' },
  ];
  
  const ocultar = () => {
    const progressLayer = document.querySelector(".Text")
    progressLayer.classList.add('hidden');
  }
  
  const handleSubmit = async (event) => {
      
    setMessages(["Filtrando Eventos..."]);
    const loadingMessages = ["Mostrando resultados..."]

    // Función para agregar mensajes uno a uno cada 1.5 segundos
    const addMessagesSequentially = (messagesArray, currentIndex) => {
      if (currentIndex < messagesArray.length) {
        setTimeout(() => {
          setMessages([]);
          setMessages((prevMessages) => [...prevMessages, messagesArray[currentIndex]]);
          addMessagesSequentially(messagesArray, currentIndex + 1);
        }, 2000);
      } else {
        // Limpiar los mensajes después de cierto tiempo
        setTimeout(() => {
          setMessages([]);
        }, 10000000); 
      }
    };

    // Comenzar a agregar mensajes secuencialmente
    addMessagesSequentially(loadingMessages, 0);



      let data = new FormData();
      data.append("file", './Run2012B_DoubleElectron.csv');
      

      try {
        const response = await fetch(import.meta.env.VITE_ENDPOINT_API+'/upload-file', {
          method: 'POST',
          body: data,
        });

        if (response.ok) {
          const jsonResponse = await response.json();
          console.log('Archivo cargado con éxito y respuesta JSON recibida del servidor');
          console.log(jsonResponse)
          ocultar();

         
          const imagenes = jsonResponse.imagenes;
          console.log(imagenes)

          const image1 = "data:image/png;base64, "+ imagenes['FourElectrons'+'Higgs_mass']
          onImage1Received(image1);
          const image2 = "data:image/png;base64, "+ imagenes['FourElectrons'+'Z1_mass']
          onImage2Received(image2);
          const image3 = "data:image/png;base64, "+ imagenes['FourElectrons'+'Z2_mass']
          onImage3Received(image3);
          const image4 = "data:image/png;base64, "+ imagenes['TwoMuonsTwoElectrons'+'Higgs_mass']
          onImage4Received(image4)
          const image5 = "data:image/png;base64, "+ imagenes['TwoMuonsTwoElectrons'+'Z1_mass']
          onImage5Received(image5);
          const image6 = "data:image/png;base64, "+ imagenes['TwoMuonsTwoElectrons'+'Z2_mass']
          onImage6Received(image6);
      
         }
         else {
          console.error('Error en la respuesta del servidor:', response.statusText);
        }

        
      } catch (error) {
        console.error('Error al cargar el archivo y recibir el JSON:', error);
      }
    
  };

  // function startProgressBar() {
  //    const btn = document.querySelector('.custom-button');
  //    var progressBar = document.getElementById('progress-bar');
  //    var messageContainer = document.getElementById('message');
  //    var progressContainer = document.getElementsByClassName('progress-container')[0];
    
  //    btn.disabled = true;
  //    btn.textContent = "Analizando..."
  //    btn.style.backgroundColor = "#ccc"
  //    btn.style.cursor = "default"
  //    // Lista de mensajes
  //    var messages = [
  //        "Analizando Imagen",
  //        "Procesando texto",
  //        "Interpretando",
  //        "Corrigiendo",
  //        "Guardando",
  //        "Imprimiendo",
  //        "Finalizado"
  //    ];
    
  //    // Función para mostrar mensajes y llenar la barra de progreso
  //    function showMessageAndFillProgressBar(index) {
  //        // Mostrar el mensaje correspondiente
  //        messageContainer.innerText = messages[index];
    
  //        // Calcular el progreso de la barra
  //        var progress = ((index + 1) / messages.length) * 100;
  //        progressBar.style.width = progress + '%';
    
  //        // let seconds = Math.round((Math.random() * 3000) + 300)
  //        let seconds = 1500;
    
  //        // Si hay más mensajes, programar el próximo
  //        if (index < messages.length - 1) {
  //            setTimeout(function () {
  //                showMessageAndFillProgressBar(index + 1);
  //            }, seconds); // Esperar 2 segundos entre cada mensaje
  //        }else{
  //          setTimeout(function () {
  //            finishLoad()
  //          }, 500);
  //        }
  //    }
    
  //    // Mostrar la barra de progreso
  //    progressContainer.style.display = 'block';
    
  //    // Iniciar el proceso de mostrar mensajes y llenar la barra de progreso
  //    setTimeout(()=>{
  //      showMessageAndFillProgressBar(0);
  //    },800);
  //   }
    
  //  function finishLoad(){
    
  //    ocultar("progress");
    
  //  }
   
  //  function ocultar(layer) {
  //    if (layer == "progress") {
      
  //      const progressLayer = document.querySelector(".progress-layer")
  //      progressLayer.classList.toggle('hidden');
  //      // document.querySelector(".hide_progress").innerHTML = (progressLayer.classList.contains('hidden')) ? '<img src="/eye.svg" alt="Ocultar" class="icon"> chat' : '<img src="/eyeSlash.svg" alt="Mostrar" class="icon"> chat';
    
  //    } else if (layer == "powerbi") {
      
  //      const pbiLayer = document.querySelector(".powerbi-layer")
  //      pbiLayer.classList.toggle('hidden');
  //      // document.querySelector(".hide_pbi").innerHTML = (pbiLayer.classList.contains('hidden')) ? '<img src="/eye.svg" alt="Ocultar" class="icon"> powerbi' : '<img src="/eyeSlash.svg" alt="Mostrar" class="icon"> powerbi';
    
  //    }
  //  }
 

  return (
    <div className="row">
  <div className="col-lg-3">
  <div className="dropdown">
      <button className={`dropdown-toggle ${selectedOption ? 'selected' : 'not-selected'}`} onClick={handleToggle}>
        {selectedOption ? selectedOption.label : 'Seleccionar opción'}
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          {options.map(option => (
            <div
              key={option.value}
              className="dropdown-item"
              onClick={() => handleOptionClick(option)}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  </div>
  <div className="col-lg-3">
      <div className="progress-layer">
              <div className="center">
                <button className="top-bar custom-button" onClick={() => { handleSubmit() }}>Clasificar Eventos</button>
              </div>
      </div>
  </div>
      <div className="col-lg-4">
        <div className="message-container">
          {messages.map((message, index) => (
            <div className="Text" key={index}>{message}</div>
          ))}
        </div>
      </div>
  </div>
  );
}

export default Botones;
 
