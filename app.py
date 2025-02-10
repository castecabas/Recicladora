from flask import Flask, render_template, Response,redirect, request, jsonify ,flash
from flask_mail import Mail,Message
from flask_caching import Cache
from flask_compress import Compress
from src.yolo_model import YOLOModel
from src.camera import Camera
import cv2
import numpy as np
import base64
import os
import re
from src.data import areas,notices,deparments,materials

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'static')
app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
Compress(app)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
app.secret_key = os.urandom(24)

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cardenas20220113@gmail.com'
app.config['MAIL_PASSWORD'] = 'bllqzryutqqmmcdh'

mail = Mail(app)

yolo_model = YOLOModel('src/model/best_yolov8n.pt')
camera = Camera()

# RUTAS
@app.route('/')
@app.route('/home')
@app.route('/index')
@cache.cached(timeout=300)
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learn')
@cache.cached(timeout=300)
def learn():
    return render_template('learn.html',areas=areas)

@app.route('/learn/plastic')
def plastic():
    return render_template('/learn_pages/plastic.html')

@app.route('/learn/glass')
def glass():
    return render_template('/learn_pages/glass.html')

@app.route('/learn/biodegradable')
def biodegradable():
    return render_template('/learn_pages/biodegradable.html')

@app.route('/learn/metal')
def metal():
    return render_template('/learn_pages/metal.html')

@app.route('/learn/cardboard')
def cardboard():
    return render_template('/learn_pages/cardboard.html')

@app.route('/learn/paper')
def paper():
    return render_template('/learn_pages/paper.html')

@app.route('/learn/nocivos')
def nocivos():
    return render_template('/learn_pages/nocivo.html')

@app.route('/model')
@cache.cached(timeout=300)
def model():
    return render_template('model.html')

@app.route('/news')
@cache.cached(timeout=300)
def news():
    return render_template('news.html',notices=notices)

@app.route('/recycle')
def recycle():
    return render_template('recycle.html')

@app.route('/recycle/recicla')
@cache.cached(timeout=300)
def recicla():
    return render_template('/recycle_pages/recicla.html',deparments=deparments)

@app.route('/recycle/reuse')
@cache.cached(timeout=300)
def reuse():
    return render_template('/recycle_pages/reuse.html',materials=materials)

@app.route('/recycle/solidarity')
def solidarity():
    return render_template('/recycle_pages/solidarity.html')

# FUNCIONES

    #NOTE: enviar al correo
@app.route('/about/send_email', methods=['GET', 'POST'])
def send_email():
    # Obtener los datos del formulario
    asunto = request.form.get('asunto')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    # Validar campos vacíos
    if not asunto or not email or not mensaje:
        flash('Completa todos los campos', 'error')
        return redirect('/about')

    # Validar formato del correo
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        flash('El correo electrónico no es válido', 'error')
        return redirect('/about')

    try:
        # Crear y enviar el mensaje
        msg = Message(asunto, sender=email, recipients=['cardenas20220113@gmail.com'])
        msg.body = mensaje
        msg.reply_to = email
        mail.send(msg)
        flash('Mensaje enviado correctamente', 'success')
        return redirect('/about')
    except Exception as e:
        flash(f'Error al enviar el mensaje: {str(e)}', 'error')
        return redirect('/about')

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
        print("==> Recibiendo petición en /detect")
        print("Content-Type:", request.headers.get("Content-Type"))

        # Procesa la petición JSON
        if request.is_json:
            data = request.get_json()
            if 'image' not in data:
                print("❌ Error: No se encontró la clave 'image' en el JSON")
                return jsonify({'error': 'No image provided in JSON'}), 400

            image_data = data['image']
            print("Imagen recibida (string largo:", len(image_data), ")")
            
            # Remover prefijo si existe
            if image_data.startswith("data:image"):
                image_data = image_data.split(",")[1]
            
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as decode_err:
                print("❌ Error decodificando base64:", decode_err)
                return jsonify({'error': 'Base64 decoding error'}), 400

            npimg = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            if img is None:
                print("❌ Error decodificando la imagen con cv2.imdecode")
                return jsonify({'error': 'Invalid image'}), 400

            confidence = float(data.get('confidence', 0.25))
            print("Confidence:", confidence)

        else:
            # Si no es JSON, se puede manejar la subida de archivos tradicional
            if 'file' not in request.files:
                print("❌ Error: No file part en form-data")
                return jsonify({'error': 'No file part'}), 400

            file = request.files['file']
            file_bytes = file.read()
            npimg = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            if img is None:
                print("❌ Error decodificando la imagen en form-data")
                return jsonify({'error': 'Invalid image'}), 400

            confidence = float(request.form.get('confidence', 0.25))
            print("Confidence:", confidence)

        # Llama a la detección del modelo
        print("Iniciando detección con el modelo...")
        results = yolo_model.detect(img, conf_threshold=confidence)
        print("Resultados:", results)
        if results is None:
            print("❌ No se obtuvieron detecciones")
            return jsonify({'error': 'No detections returned from model'}), 500

        # Dibuja las detecciones sobre la imagen
        processed_img = yolo_model.draw_boxes(img, results)

        # Codifica la imagen procesada en base64
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        print("Envío de respuesta exitoso")
        
        return jsonify({
            'image': f'data:image/jpeg;base64,{img_base64}',
            'detections': results
        })

    except Exception as e:
        print("❌ Error durante la detección:", e)
        # Es importante retornar un JSON válido incluso en error
        return jsonify({'error': f'Error during detection: {e}'}), 500

    
# EJECUCION
if __name__ == '__main__':
    
    app.run(port=5000,debug=True)