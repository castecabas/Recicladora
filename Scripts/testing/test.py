
from ultralytics import YOLO


model = YOLO("C:/Users/castecabas/Desktop/PROYECTOS/Recicladora/Scripts/trainer/runs/detect/train3/weights/last.pt")

results= model.predict(source="1",show=True,imgsz=640,conf=0.5)

print(results)