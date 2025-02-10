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
import gdown
from src.data import areas,notices,deparments,materials

DEBUG_MODE = False

# ID del archivo de Google Drive
FILE_ID = "1OWhwS6v-VyU4lTBF8UgZ81pp7S_rnlKA"
MODEL_PATH = "best_yolov11.pt"  # Cambia esto según tu modelo

# Verifica si el modelo ya existe, si no, lo descarga
if not os.path.exists(MODEL_PATH):
    print("Descargando modelo desde Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", MODEL_PATH, quiet=False)
    print("Modelo descargado con éxito.")


# Suponiendo que tu script se ejecuta desde la raíz o se conoce la ruta base:
# Si este script está en la raíz, puedes definir la ruta base así:
base_dir = os.path.join("/tmp", "Recicladora")

# Configuración para Matplotlib:
matplotlib_config_dir = os.path.join(base_dir, "config", "matplotlib")
os.makedirs(matplotlib_config_dir, exist_ok=True)  # Crea el directorio si no existe
os.environ["MPLCONFIGDIR"] = matplotlib_config_dir

# Configuración para Ultralytics:
ultralytics_config_dir = os.path.join(base_dir, "config", "ultralytics")
os.makedirs(ultralytics_config_dir, exist_ok=True)  # Crea el directorio si no existe
os.environ["ULTRALYTICS_HOME"] = ultralytics_config_dir

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

yolo_model = YOLOModel('best_yolov11.pt')
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
        if DEBUG_MODE: print("==> Recibiendo petición en /detect")

        content_type = request.headers.get("Content-Type")
        if DEBUG_MODE: print("Content-Type:", content_type)

        image_data, confidence = None, 0.25

        # Procesar JSON (imagen en base64)
        if request.is_json:
            data = request.get_json()
            image_data = data.get('image')
            confidence = float(data.get('confidence', 0.25))

            if not image_data:
                return jsonify({'error': 'No image provided in JSON'}), 400

            # Remover prefijo "data:image/..." si existe
            if image_data.startswith("data:image"):
                image_data = image_data.split(",")[-1]

            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as decode_err:
                return jsonify({'error': 'Base64 decoding error'}), 400

        # Procesar form-data (archivo de imagen)
        else:
            file = request.files.get('file')
            if not file:
                return jsonify({'error': 'No file provided'}), 400
            image_bytes = file.read()
            confidence = float(request.form.get('confidence', 0.25))

        # Decodificar imagen
        npimg = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'error': 'Invalid image'}), 400

        # Reducir tamaño de la imagen para acelerar inferencia
        img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_AREA)

        if DEBUG_MODE: print(f"Iniciando detección con confianza {confidence}...")

        # Llamada al modelo
        results = yolo_model.detect(img, conf_threshold=confidence)
        if results is None:
            return jsonify({'error': 'No detections returned from model'}), 500

        # Dibujar detecciones
        processed_img = yolo_model.draw_boxes(img, results)

        # Codificar imagen de salida en base64 (solo si es necesario)
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'image': f'data:image/jpeg;base64,{img_base64}',
            'detections': results
        })

    except Exception as e:
        return jsonify({'error': f'Error during detection: {str(e)}'}), 500

    
# EJECUCION
if __name__ == '__main__':
    
    app.run(port=5000,debug=True)