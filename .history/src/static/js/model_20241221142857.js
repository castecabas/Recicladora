let currentCameraIndex = 0;
let cameras = [];
const clsname = [
    "Comida", "Planta", "Fruta o Verdura", "Base de Carton", "Caja de Carton", 
    "Contenedor de Carton", "Forma de Carton", "Botella de Vidrio", "Vajilla de Vidrio", 
    "Fragmentos de Vidrio", "Frasco de Vidrio", "Jarra de Vidrio", "Aluminio", 
    "Contenedor Metalico", "Latas de Alimento", "Menaje Metalico", "Metal Menor", 
    "Utensilio Metalico", "Bateria o Pila", "Carta de Papel", "Recibo o Factura", 
    "Periodico o Revista", "Forma de Papel", "Papel de Higiene", "Bolsa de Plastico", 
    "Botella de Plastico", "Contenedor de Plastico", "Envase de Plastico", 
    "Vajilla de Plastico", "Tapa de Plastico", "Utensilio de Plastico"
  ];
let confidenceThreshold = 0.5;

const parrafo = document.getElementById("confidenceValue");

const valorDecimal = parseFloat(parrafo.textContent);
const valorPorcentaje = valorDecimal * 100;
parrafo.textContent = valorPorcentaje + "%";

document.addEventListener('DOMContentLoaded', function () {
    fetchCameras();

    document.getElementById('switchCameraBtn').addEventListener('click', switchCamera);
    document.getElementById('captureBtn').addEventListener('click', captureAndDetect);
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);

    const confidenceSlider = document.getElementById('confidenceThreshold');
    const confidenceValue = document.getElementById('confidenceValue');

    confidenceSlider.addEventListener('input', function () {
        confidenceThreshold = parseFloat(this.value);
        confidenceValue.textContent = confidenceThreshold.toFixed(2);
        const valorDecimal = parseFloat(parrafo.textContent);
        const valorPorcentaje = valorDecimal * 100;
        parrafo.textContent = valorPorcentaje.toFixed(0) + "%";
    });
});

function fetchCameras() {
    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            cameras = devices.filter(device => device.kind === 'videoinput');
            updateCurrentCamera();
        })
        .catch(error => {
            console.error('Error enumerating devices:', error);
        });
}

async function switchCamera() {
    currentCameraIndex = (currentCameraIndex + 1) % cameras.length;
    updateCurrentCamera();

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { deviceId: { ideal: cameras[currentCameraIndex].deviceId } }
        });
        document.getElementById('video').srcObject = stream;
    } catch (error) {
        console.error('Error switching camera:', error);
    }
}

function updateCurrentCamera() {
    const cameraInfo = cameras[currentCameraIndex] ? cameras[currentCameraIndex].label : 'Unknown';
    document.getElementById('currentCamera').textContent = cameraInfo;
}

function captureAndDetect() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.jpg');
        formData.append('confidence', confidenceThreshold);
        detectObjects(formData);
    }, 'image/jpeg');
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('confidence', confidenceThreshold);
    detectObjects(formData);
}

function detectObjects(formData) {
    fetch('/detect', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultImage').src = data.image;
            updateDetectionsList(data.detections);
        })
        .catch(error => {
            console.error('Error detecting objects:', error);
        });
}

function updateDetectionsList(detections) {
    const list = document.getElementById('detectionsList');
    list.innerHTML = '';
    detections.forEach(detection => {
        const [x1, y1, x2, y2, conf, cls] = detection;
        const li = document.createElement('li');
        li.classList.add(clsname[cls].toLowerCase());
        li.textContent = `Clase: ${clsname[cls] || 'Desconocido'}, Confianza: ${conf.toFixed(2) * 100} %`;
        list.appendChild(li);
    });
}

async function initializeCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        document.getElementById('video').srcObject = stream;
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
}

function openNav() {
    document.getElementById("aside").style.width = "250px";
}

function closeNav() {
    document.getElementById("aside").style.width = "0";
}

initializeCamera();