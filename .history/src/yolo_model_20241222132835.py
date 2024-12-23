from ultralytics import YOLO
import cv2
import numpy as np

class YOLOModel:
    def __init__(self, model_path):
        # Cargar el modelo YOLO
        self.model = YOLO(model_path)

        # Colores de cada clase en BGR
        self.colors = [
            (0, 204, 102), (0, 204, 102), (0, 204, 102),  # Verde brillante (Biodegradable)
            (153, 102, 51), (153, 102, 51), (153, 102, 51),  # Marrón cálido (Cartón)
            (192, 192, 192), (192, 192, 192), (192, 192, 192), (192, 192, 192), (192, 192, 192),  # Gris metálico (Metal)
            (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255),  # Azul intenso (Vidrio)
            (255, 51, 51),  # Rojo vibrante (Nocivo)
            (255, 255, 102), (255, 255, 102), (255, 255, 102), (255, 255, 102), (255, 255, 102),  # Amarillo claro (Papel)
            (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255)  # Naranja fuerte (Plástico)
        ]

    def detect(self, image, conf_threshold=0.5):
        # Realizar detecciones con el modelo YOLO
        results = self.model(image, conf=conf_threshold)
        return results[0].boxes.data.tolist()

    def draw_boxes(self, image, results):
        # Obtener las dimensiones de la imagen
        height, width = image.shape[:2]

        for r in results:
            x1, y1, x2, y2, conf, cls = r

            # Calcular el grosor del bounding box de manera dinámica
            box_width = x2 - x1
            box_height = y2 - y1
            thickness = max(1, int(min(box_width, box_height) / 50))

            # Calcular el tamaño del texto (font_scale) dinámicamente
            font_scale = min(box_width, box_height) / 200
            font_scale = max(0.5, min(font_scale, 1))

            # Calcular el grosor del texto dinámicamente
            text_thickness = max(1, int(thickness / 2))

            # Obtener el color del bounding box y texto (en BGR)
            color = self.colors[int(cls) % len(self.colors)]

            # Dibujar el bounding box
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

            # Preparar el texto para dibujar
            text = f"{self.model.names[int(cls)]} : {conf:.2f}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)
            text_width, text_height = text_size

            # Asegurarse que el texto no se salga de los bordes de la imagen
            text_x = max(0, min(int(x1), width - text_width))
            text_y = max(text_height + 10, min(int(y1) - 10, height - text_height))

            # Dibujar un fondo para el texto
            cv2.rectangle(image, (text_x, text_y - text_height - 5), (text_x + text_width, text_y + 5), color, -1)

            # Dibujar el texto sobre el fondo
            #cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), text_thickness)

        return image


