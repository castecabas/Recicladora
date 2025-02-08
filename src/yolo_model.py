from ultralytics import YOLO
import cv2
import numpy as np

class YOLOModel:
    def __init__(self, model_path):
        # Cargar el modelo YOLO
        self.model = YOLO(model_path)

        # Colores para cada clase
        self.colors = [
    (0, 204, 102), (0, 204, 102), (0, 204, 102), 
    (153, 102, 51), (153, 102, 51), (153, 102, 51), (153, 102, 51),
    (0, 128, 255),(0, 128, 255),(0, 128, 255),(0, 128, 255),(0, 128, 255),
    (192, 192, 192),(192, 192, 192),(192, 192, 192),(192, 192, 192),(192, 192, 192),(192, 192, 192),
    (255, 51, 51), 
    (255, 255, 102), (255, 255, 102), (255, 255, 102), (255, 255, 102), (255, 255, 102),  
    (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0)
]

    def detect(self, image, conf_threshold=0.5):
        try:
            results = self.model(image, conf=conf_threshold)[0]  # Tomar solo el primer resultado
            if not hasattr(results, 'boxes') or results.boxes is None:
                return []
            
            detections = []
            for box in results.boxes.data.tolist():
                if len(box) >= 6:
                    x1, y1, x2, y2, conf, cls = box[:6]
                    detections.append([x1, y1, x2, y2, conf, int(cls)])

            return detections
        except Exception as e:
            print(f"Error en la detección: {e}")
            return []

    def draw_boxes(self, image, results):
        height, width = image.shape[:2]
    
        for r in results:
            x1, y1, x2, y2, conf, cls = r
            cls = int(cls)

            # Validar que la clase existe en el modelo
            class_name = self.model.names.get(cls, "Desconocido")

            # Calcular grosor dinámico y tamaño de fuente
            box_width = x2 - x1
            box_height = y2 - y1
            thickness = max(1, int(min(box_width, box_height) / 50))
            font_scale = max(0.5, min(box_width / 200, 1))
            text_thickness = max(1, thickness // 2)

            # Color de la caja y texto
            color = self.colors[cls % len(self.colors)]
            color_bgr = (color[2], color[1], color[0])

            # Dibujar el bounding box
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color_bgr, thickness)

            # Texto de la detección
            text = f"{class_name}: {conf:.2f}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)
            text_width, text_height = text_size

            # Ajustar posición del texto
            text_x = max(int(x1), min(int(x1), width - text_width))
            text_y = max(int(y1) - 10, min(int(y1) - 10, height - text_height))

            # Dibujar fondo del texto y texto
            #cv2.rectangle(image, (text_x, text_y - text_height), (text_x + text_width, text_y), color_bgr, -1)
            #cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), text_thickness)

        return image
