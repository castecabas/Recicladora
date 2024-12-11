import os
from PIL import Image

def convert_and_rename_images(folder_path, name_base, resize,count):
    # Crear el directorio de salida
    output_folder = os.path.join(folder_path, "converted")
    os.makedirs(output_folder, exist_ok=True)

    # Obtener todos los archivos en el directorio
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    
    for file in files:
        file_path = os.path.join(folder_path, file)

        # Ignorar archivos ocultos
        if file.startswith("."):
            continue

        try:
            # Abrir imagen y convertirla a JPG
            with Image.open(file_path) as img:
                # Convertir la imagen al modo RGB si no lo está
                img = img.convert("RGB")

                # Obtener las dimensiones originales
                width, height = img.size

                # Redimensionar la imagen solo si su resolución es superior
                if width > resize or height > resize:
                    aspect_ratio = width / height
                    if aspect_ratio > 1:
                        # Landscape
                        new_width = resize
                        new_height = int(resize / aspect_ratio)
                    else:
                        # Portrait or square
                        new_height = resize
                        new_width = int(resize * aspect_ratio)

                    img = img.resize((new_width, new_height))

                # Crear el nuevo nombre y ruta
                new_name = f"{name_base}_{count}.jpg"
                output_path = os.path.join(output_folder, new_name)

                # Guardar como JPG
                img.save(output_path, "JPEG")
                print(f"Convertido: {file} -> {new_name}")

                count += 1

        except Exception as e:
            print(f"Error al procesar el archivo {file}: {e}")


# Uso del script
folder_path = "C:/Users/castecabas/Desktop/PROYECTOS/Recicladora/Dataset/ImageConverter"  # Cambia esto a la ruta de tu carpeta
img_resolution=1080
name_base = ""  #poner nombre inicial que se va a iterar
count=501
convert_and_rename_images(folder_path, name_base, img_resolution,count)

