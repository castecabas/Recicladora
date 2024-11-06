from flask import Flask, render_template, Response, request, jsonify
from yolo_model import YOLOModel
from camera import Camera
import cv2
import numpy as np
import base64

app = Flask(__name__)

yolo_model = YOLOModel('src/model/best.pt')
camera = Camera()

# RUTAS
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/recycle')
def recycle():
    return render_template('recycle.html')

@app.route('/recycle/recicla')
def recicla():
    return render_template('/recycle_pages/recicla.html')

@app.route('/recycle/reuse')
def reuse():
    return render_template('/recycle_pages/reuse.html')

@app.route('/recycle/solidarity')
def solidarity():
    return render_template('/recycle_pages/solidarity.html')

# FUNCIONES

    #NOTE: obtener las camaras
@app.route('/get_cameras')
def get_cameras():
    return jsonify(camera.get_camera_list())

    #NOTE: cambiar camara
@app.route('/switch_camera/<int:camera_id>')
def switch_camera(camera_id):
    camera.select_camera(camera_id)
    return "OK"

    #NOTE: detectar dicha imagen
@app.route('/detect', methods=['POST'])
def detect():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        confidence = float(request.form.get('confidence', 0.25))

        # Lee la imagen del archivo
        npimg = np.fromfile(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        # Detecta objetos usando el modelo YOLO
        results = yolo_model.detect(img, conf_threshold=confidence)
        if results is None:
            return jsonify({'error': 'No detections returned from model'}), 500

        # Dibuja los cuadros de detección en la imagen
        processed_img = yolo_model.draw_boxes(img, results)

        # Codifica la imagen procesada en base64 para enviar al cliente
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'image': f'data:image/jpeg;base64,{img_base64}',
            'detections': results
        })
    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({'error': str(e)}), 500
    
# EJECUCION
if __name__ == '__main__':
    app.run(debug=True)