from ultralytics import YOLO
import torch
import torchvision
import os

if __name__ == '__main__':
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    torch.cuda.is_available()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("PyTorch version:", torch.__version__)
    print("Torchvision version:", torchvision.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("CUDA version:", torch.version.cuda)
    print(f"Using device: {device}")

    logdir = "C:/Users/castecabas/Desktop/PROYECTOS/Recicladora/Scripts/trainer/runs/detect/train"  # Directorio donde se guardarán los logs de TensorBoard
    os.makedirs(logdir, exist_ok=True)

    # Entrenar con dicho modelo ("Ruta o modelo vacio")
    model = YOLO("yolo11n.pt")

    model.train(
        data="C:/Users/castecabas/Desktop/PROYECTOS/Recicladora/Dataset/dataset.yaml", #colocar su Data.yaml
        batch=8,
        imgsz=640,
        workers=6,
        epochs=200,
        patience=30,
        optimizer="AdamW",
        augment=True,
        dropout=0.2,
        device=0,
        lr0=0.001,
        weight_decay=0.001,
        cos_lr=True,
        warmup_epochs=5,
        hsv_h=0.02,        # Variación de matiz para data augmentation
        hsv_s=0.8,          # Variación de saturación para data augmentation
        hsv_v=0.5,          # Variacion de Brillo
        degrees=15,
        shear=10,
        flipud=0.1,
        perspective=0.0005,
        mixup=0.1,
        copy_paste=0.2,
        cache=True,
        save=True,
        resume=True
    )