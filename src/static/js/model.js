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

document.addEventListener('DOMContentLoaded', function () {
    fetchCameras();

    document.getElementById('switchCameraBtn').addEventListener('click', switchCamera);
    document.getElementById('captureBtn').addEventListener('click', captureAndDetect);
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);

    const confidenceSlider = document.getElementById('confidenceThreshold');
    const confidenceValue = document.getElementById('confidenceValue');

    confidenceSlider.addEventListener('input', function () {
        confidenceThreshold = parseFloat(this.value);
        confidenceValue.textContent = (confidenceThreshold * 100).toFixed(0) + "%";
    });
});

function fetchCameras() {
    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            cameras = devices.filter(device => device.kind === 'videoinput');
            currentCameraIndex = cameras.length > 0 ? 0 : -1;
            updateCurrentCamera();
        })
        .catch(error => console.error('Error enumerando dispositivos:', error));
}

async function switchCamera() {
    if (cameras.length === 0) return;
    
    currentCameraIndex = (currentCameraIndex + 1) % cameras.length;
    updateCurrentCamera();

    try {
        // Detener el stream actual si existe
        const video = document.getElementById('video');
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }

        // Configurar las restricciones para la cámara
        const constraints = {
            video: {
                deviceId: { exact: cameras[currentCameraIndex].deviceId },
                facingMode: undefined // Inicialmente undefined
            }
        };

        // Intentar determinar si es una cámara trasera
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        if (isMobile) {
            const label = cameras[currentCameraIndex].label.toLowerCase();
            if (label.includes('back') || label.includes('trasera') || label.includes('rear')) {
                constraints.video.facingMode = 'environment';
            } else if (label.includes('front') || label.includes('frontal')) {
                constraints.video.facingMode = 'user';
            }
        }

        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
    } catch (error) {
        console.error('Error al cambiar de cámara:', error);
        // Intentar con configuración alternativa si falla
        try {
            const alternativeConstraints = {
                video: {
                    facingMode: currentCameraIndex % 2 === 0 ? 'user' : 'environment'
                }
            };
            const stream = await navigator.mediaDevices.getUserMedia(alternativeConstraints);
            document.getElementById('video').srcObject = stream;
        } catch (fallbackError) {
            console.error('Error en fallback de cámara:', fallbackError);
        }
    }
}

function updateCurrentCamera() {
    const cameraInfo = cameras[currentCameraIndex] ? cameras[currentCameraIndex].label : 'No disponible';
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
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        // e.target.result contiene la imagen en formato Data URL (por ejemplo: "data:image/jpeg;base64,/9j/...")
        const base64Image = e.target.result;

        // Ahora enviamos la imagen y la confianza en formato JSON
        sendDetectionRequestJSON(base64Image, confidenceThreshold);
    };
    reader.readAsDataURL(file);
}

function sendDetectionRequestJSON(base64Image, confidence) {
    fetch('/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            image: base64Image,  // Enviamos la imagen codificada en Base64
            confidence: confidence  // Enviamos el valor de confianza
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultImage').src = data.image;
        updateDetectionsList(data.detections);
    })
    .catch(error => console.error('Error detectando objetos:', error));
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
    .catch(error => console.error('Error detectando objetos:', error));
}

function updateDetectionsList(detections) {
    const list = document.getElementById('detectionsList');
    list.innerHTML = '';
    detections.forEach(detection => {
        const [x1, y1, x2, y2, conf, cls] = detection;
        const li = document.createElement('li');
        li.textContent = `Clase: ${clsname[cls] || 'Desconocido'}, Confianza: ${(conf * 100).toFixed(0)} %`;
        list.appendChild(li);
    });
}

async function initializeCamera() {
    try {
        if (document.getElementById('video').srcObject) return; // Evita reiniciar el stream si ya está en uso

        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        document.getElementById('video').srcObject = stream;
    } catch (error) {
        console.error('Error accediendo a la cámara:', error);
    }
}

function openNav() {
    document.getElementById("aside").style.width = "250px";
}

function closeNav() {
    document.getElementById("aside").style.width = "0";
}

initializeCamera();
