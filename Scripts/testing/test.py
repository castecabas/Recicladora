
from ultralytics import YOLO


model = YOLO("C:/Users/castecabas/PycharmProjects/Recycler_Proyect/S_Training/runs/detect/train6/weights/best.pt")

results= model.predict(source="0",show=True,imgsz=640,conf=0.5)

print(results)