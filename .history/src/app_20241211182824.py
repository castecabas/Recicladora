from flask import Flask, render_template, Response,redirect, request, jsonify ,flash
from flask_mail import Mail,Message
from yolo_model import YOLOModel
from camera import Camera
import cv2
import numpy as np
import base64
import os
import re

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cardenas20220113@gmail.com'
app.config['MAIL_PASSWORD'] = 'bllqzryutqqmmcdh'

mail = Mail(app)

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
    areas=[
    {
        'title':'Plastico',
        'description':'Aprende sobre los diferentes tipos de plásticos, sus usos comunes, y el impacto ambiental que generan.'
    },
    {
        'title':'Vidrio',
        'description':'Conoce su proceso de reciclaje y los beneficios de reutilizar este material, que contribuye a un entorno más sostenible.'
    },
    {
        'title':'Biodegradable',
        'description':'Conoce qué significa realmente que un material sea biodegradable y su importancia en la reducción de residuos'
    },
    {
        'title':'Metal',
        'description':'Aprende sobre los tipos de metales que se encuentran en productos de uso diario y su importancia en el reciclaje.'
    },
    {
        'title':'Carton',
        'description':'Descubre por qué el cartón es uno de los materiales reciclables más comunes y fáciles de reutilizar'
    },
    {
        'title':'',
        'description':''
    },
    {
        'title':'',
        'description':''
    }
    ]
    return render_template('learn.html')

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