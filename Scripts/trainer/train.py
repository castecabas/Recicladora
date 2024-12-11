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
        batch=4,
        workers=8,
        epochs=100,
        patience=15,
        optimizer="Adam",
        augment=True,
        dropout=0.5,
        device=0
    )