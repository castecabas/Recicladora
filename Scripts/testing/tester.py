# Importamos librerías
import torch.hub
from ultralytics import YOLO
import cv2

model = YOLO('C:/Users/castecabas/Desktop/best.pt')

# Captura de Camara
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
capture.set(10,100)

# Clases
clsName = ['Biodegradable', 'Carton', 'Vidrio', 'Metal', 'Papel', 'Plastico']  # modelos S
#clsName = ['Carton','Papel','Plastico','Metal','Vidrio','Basura']  # modelos M

# Colores para cada clase
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

#Bucle del programa
while True:
    # Leer frame de la cámara
    ret, frame = capture.read()
    if not ret:
        print("No se pudo capturar el video.")
        break
    with torch.amp.autocast(device_type='cuda'):
        # Realizar la inferencia con YOLOv5
        results = model(frame)

    # Yolo | AntiSpoof
    results = model(frame, stream=True, verbose=False)
    for result in results:
        # Boxes
        for box in result.boxes:
            # Bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Asegurar que las coordenadas sean válidas
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = max(0, x2), max(0, y2)

            # Clase y confianza
            cls = int(box.cls[0])
            conf = box.conf[0]
            print(f"Clase: {clsName[cls]} Confidence: {conf:.2f}")

            # Dibujar el cuadro y la etiqueta si la confianza es alta
            if conf > 0.36: #0.36 esta bien
                color = colors[cls]  # Color basado en la clase
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f'{clsName[cls]} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        # Mostrar el frame con las detecciones
    cv2.imshow("Detector", frame)
        # Cerrar con la tecla 'ESC'
    if cv2.waitKey(5) & 0xFF == 27:
     break


capture.release()
cv2.destroyAllWindows()