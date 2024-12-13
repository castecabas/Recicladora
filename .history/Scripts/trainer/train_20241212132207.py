from ultralytics import YOLO
import torch
import os

if __name__ == '__main__':

    torch.cuda.is_available()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    logdir = "C:/Users/castecabas/Desktop/PROYECTOS/Recicladora/Scripts/trainer/runs/detect/train"  # Directorio donde se guardarán los logs de TensorBoard
    os.makedirs(logdir, exist_ok=True)

    # Entrenar con dicho modelo ("Ruta o modelo vacio")
    model = YOLO("yolov11n.pt")

    model.train(
        data="", #colocar su Data.yaml
        batch=8,
        imgsz=640,
        workers=6,
        epochs=500,
        patience=100,
        optimizer="AdamW",
        augment=True,
        dropout=0.2,
        device=0,
        lr0=0.001,
        weight_decay=0.001,
        cos_lr=True
    )