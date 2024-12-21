from ultralytics import YOLO
import cv2
import numpy as np

class YOLOModel:
    def __init__(self, model_path):

        #NOTE: Ruta del modelo
        self.model = YOLO(model_path)
        
        #NOTE: Colores de cada clase en RGB
        self.colors = [
  "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
  "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
  "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
  "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080",
  "#ff5050", "#99ff99", "#ffcc00", "#6699ff", "#cc33ff",
  "#33cccc", "#ff6666", "#99cc33", "#9933ff", "#ffcc99",
  "#00bfff"
]

    def detect(self, image, conf_threshold=0.5):
        results = self.model(image, conf=conf_threshold)
        return results[0].boxes.data.tolist()

    def draw_boxes(self, image, results):
        for r in results:
            x1, y1, x2, y2, conf, cls = r
            color = self.colors[int(cls) % len(self.colors)]
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
            cv2.putText(image, f"{self.model.names[int(cls)]} : {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return image