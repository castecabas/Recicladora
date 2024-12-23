from ultralytics import YOLO
import cv2
import numpy as np

class YOLOModel:
    def __init__(self, model_path):
        # Ruta del modelo
        self.model = YOLO(model_path)

        # Colores de cada clase en RGB
        self.colors = [
    (0, 0, 0), (0, 204, 102), (0, 204, 102),  # Verde brillante (Biodegradable)
    (153, 102, 51), (153, 102, 51), (153, 102, 51),  # Marrón cálido (Cartón)
    (192, 192, 192), (192, 192, 192), (192, 192, 192), (192, 192, 192), (192, 192, 192),  # Gris metálico (Metal)
    (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255), (0, 128, 255),  # Azul intenso (Vidrio)
    (255, 51, 51),  # Rojo vibrante (Nocivo)
    (255, 255, 102), (255, 255, 102), (255, 255, 102), (255, 255, 102), (255, 255, 102),  # Amarillo claro (Papel)
    (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0), (255, 128, 0)  # Naranja fuerte (Plástico)
]

    def detect(self, image, conf_threshold=0.5):
        results = self.model(image, conf=conf_threshold)
        return results[0].boxes.data.tolist()

    def draw_boxes(self, image, results):
        # Dimensiones de la imagen
        height, width = image.shape[:2]
        
        for r in results:
            x1, y1, x2, y2, conf, cls = r
            
            # Calcular el grosor dinámico para el bounding box
            box_width = x2 - x1
            box_height = y2 - y1
            thickness = max(1, int(min(box_width, box_height) / 50))  # Ajuste dinámico para el grosor del bounding box
            
            # Calcular el tamaño del texto (font_scale) dinámicamente basado en el tamaño del bounding box
            font_scale = min(box_width, box_height) / 200  # Ajuste del tamaño del texto en función del tamaño del bounding box
            font_scale = max(0.5, min(font_scale, 1))  # Limitar el tamaño de fuente para que no sea demasiado grande

            # Calcular el grosor del texto dinámicamente
            text_thickness = max(1, int(thickness / 2))  # Grosor del texto en función del grosor del bounding box
            
            # Calcular color del bounding box y texto
            color = self.colors[int(cls) % len(self.colors)]

            # Dibujar el bounding box con grosor dinámico
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

            # Calcular la posición del texto asegurándose que no se salga de la imagen
            text = f"{self.model.names[int(cls)]} : {conf:.2f}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)
            text_width, text_height = text_size

            # Asegurarse que el texto no se salga de la imagen
            text_x = max(int(x1), min(int(x1), width - text_width))
            text_y = max(int(y1) - 10, min(int(y1) - 10, height - text_height))

            # Dibujar el texto con grosor y tamaño dinámico
            # cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, text_thickness)
        
        return image


