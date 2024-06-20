import React from 'react';
import '../App.css';
import '../App.jsx';

export const ProgressBar = () => {
   function startProgressBar() {
    const btn = document.querySelector('.custom-button');
    var progressBar = document.getElementById('progress-bar');
    var messageContainer = document.getElementById('message');
    var progressContainer = document.getElementsByClassName('progress-container')[0];
   
    btn.disabled = true;
    btn.textContent = "Analizando..."
    btn.style.backgroundColor = "#ccc"
    btn.style.cursor = "default"
    // Lista de mensajes
    var messages = [
        "Analizando Imagen",
        "Procesando texto",
        "Interpretando",
        "Corrigiendo",
        "Guardando",
        "Imprimiendo",
        "Finalizado"
    ];
   
    // Función para mostrar mensajes y llenar la barra de progreso
    function showMessageAndFillProgressBar(index) {
        // Mostrar el mensaje correspondiente
        messageContainer.innerText = messages[index];
   
        // Calcular el progreso de la barra
        var progress = ((index + 1) / messages.length) * 100;
        progressBar.style.width = progress + '%';
   
        // let seconds = Math.round((Math.random() * 3000) + 300)
        let seconds = 1500;
   
        // Si hay más mensajes, programar el próximo
        if (index < messages.length - 1) {
            setTimeout(function () {
                showMessageAndFillProgressBar(index + 1);
            }, seconds); // Esperar 2 segundos entre cada mensaje
        }else{
          setTimeout(function () {
            finishLoad()
          }, 500);
        }
    }
   
    // Mostrar la barra de progreso
    progressContainer.style.display = 'block';
   
    // Iniciar el proceso de mostrar mensajes y llenar la barra de progreso
    setTimeout(()=>{
      showMessageAndFillProgressBar(0);
    },800);
  }
   
  function finishLoad(){
   
    ocultar("progress");
   
  }
  
  function ocultar(layer) {
    if (layer == "progress") {
     
      const progressLayer = document.querySelector(".progress-layer")
      progressLayer.classList.toggle('hidden');
      // document.querySelector(".hide_progress").innerHTML = (progressLayer.classList.contains('hidden')) ? '<img src="/eye.svg" alt="Ocultar" class="icon"> chat' : '<img src="/eyeSlash.svg" alt="Mostrar" class="icon"> chat';
   
    } else if (layer == "powerbi") {
     
      const pbiLayer = document.querySelector(".powerbi-layer")
      pbiLayer.classList.toggle('hidden');
      // document.querySelector(".hide_pbi").innerHTML = (pbiLayer.classList.contains('hidden')) ? '<img src="/eye.svg" alt="Ocultar" class="icon"> powerbi' : '<img src="/eyeSlash.svg" alt="Mostrar" class="icon"> powerbi';
   
    }
  }
  


  return (
      <div>
            <div className="progress-layer">
              <div className="center">
                <button className="top-bar custom-button" onClick={startProgressBar}>Analizar</button>
                <startProgressBar/>
              </div>
                  <div className="progress-container">
                      <div className="progress-bar" id="progress-bar"></div>
                  </div>
                  <div id="message"></div>
              </div>
          <div className="column chat-layer">
              <div id="chat_component"></div>
          </div>
      </div>
  )
}

