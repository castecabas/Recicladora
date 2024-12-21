from ultralytics import YOLO
import cv2
import numpy as np

class YOLOModel:
    def __init__(self, model_path):
        # Ruta del modelo
        self.model = YOLO(model_path)

        # Colores de cada clase en RGB
        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
            (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
            (0, 128, 128), (128, 0, 128), (255, 128, 0), (128, 255, 0), (0, 255, 128),
            (128, 0, 255), (0, 128, 255), (255, 0, 128), (192, 192, 192), (128, 128, 128),
            (255, 192, 203), (75, 0, 130), (255, 20, 147), (139, 69, 19), (50, 205, 50),
            (0, 100, 0), (47, 79, 79), (70, 130, 180), (210, 105, 30), (244, 164, 96),
            (255, 228, 181)
        ]

    def detect(self, image, conf_threshold=0.5):
        results = self.model(image, conf=conf_threshold)
        return results[0].boxes.data.tolist()

    def draw_boxes(self, image, results):
        # Dimensiones de la imagen
        height, width = image.shape[:2]
        
        for r in results:
            x1, y1, x2, y2, conf, cls = r
            
            # Calcular grosor dinámico basado en la resolución
            box_width = x2 - x1
            box_height = y2 - y1
            thickness = max(1, int(min(box_width, box_height) / 50))  # Ajuste dinámico para el grosor
            
            # Calcular tamaño de texto dinámico basado en el tamaño del bounding box
            font_scale = max(0.5, min(box_height, box_width) / 100)  # Ajuste dinámico para el texto
            
            # Calcular color del bounding box y texto
            color = self.colors[int(cls) % len(self.colors)]
            
            # Dibujar el bounding box con grosor dinámico
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
            
            # Dibujar el texto con tamaño dinámico
            cv2.putText(image, f"{self.model.names[int(cls)]} : {conf:.2f}", 
                        (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        font_scale, color, (thickness+0.2))
        
        return image

