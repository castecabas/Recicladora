let currentCameraIndex = 0;
let cameras = [];
const clsname = ['Biodegradable', 'Carton', 'Vidrio', 'Metal', 'Papel', 'Plastico'];
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
        alert('Failed to switch camera. Please try again.');
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
            alert('Failed to detect objects. Please try again.');
        });
}

function updateDetectionsList(detections) {
    const list = document.getElementById('detectionsList');
    list.innerHTML = '';
    detections.forEach(detection => {
        const [x1, y1, x2, y2, conf, cls] = detection;
        const li = document.createElement('li');
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
        alert('Failed to access camera. Please check your camera permissions.');
    }
}

function openNav() {
    document.getElementById("aside").style.width = "250px";
}

function closeNav() {
    document.getElementById("aside").style.width = "0";
}

initializeCamera();