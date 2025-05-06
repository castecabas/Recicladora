#  🌱 Proyecto Recicladora 🌱

  Es un trabajo de tesis tecnologica donde presenta un aplicativo web y movil, en el cual presenta un modelo neuronal YOLO (version 11 - nano) en el cual es utilizado como objetivo en la deteccion de materiales reciclables.

  Ademas presentan informacion de aprendizaje ,conocimiento y soluciones con las materias enfocado en Colombia.

  Se va a tener en cuenta las siguientes clases:

| Categoría               | Subcategoría               |
|-------------------------|---------------------------|
| **Biodegradable**       | Comida                    |
|                         | Planta                    |
|                         | Fruta o Verdura           |
| **Cartón**              | Base de Cartón            |
|                         | Caja de Cartón            |
|                         | Contenedor de Cartón      |
|                         | Forma de Cartón           |
| **Vidrio**              | Botella de Vidrio         |
|                         | Vajilla de Vidrio         |
|                         | Fragmentos de Vidrio      |
|                         | Frasco de Vidrio          |
|                         | Jarra de Vidrio           |
| **Metal**               | Aluminio                  |
|                         | Contenedor Metálico       |
|                         | Latas de Alimento         |
|                         | Menaje Metálico           |
|                         | Metal Menor               |
|                         | Utensilio Metálico        |
| **Nocivo**              | Batería o Pila            |
| **Papel**               | Carta de Papel            |
|                         | Recibo o Factura          |
|                         | Periódico o Revista       |
|                         | Forma de Papel            |
|                         | Papel de Higiene          |
| **Plástico**            | Bolsa de Plástico         |
|                         | Botella de Plástico       |
|                         | Contenedor de Plástico    |
|                         | Envase de Plástico        |
|                         | Vajilla de Plástico       |
|                         | Tapa de Plástico          |
|                         | Utensilio de Plástico     |


 # Requisitos de instalacion 
1. Clona el respositorio (Boton Verde "<> Code").

  ° Opcion 1: Por Codigo
  
  ° Opcion 2: Descargando el .ZIP

2. Se debe Tener instalado un IDE y Python (Preferente v3.9.0)

La estructura se Descomponen de lo siguiente:

  ° Carpeta SRC -> abarca todo lo relacionado con el aplicativo web.

  ° Carpeta Scripts -> abarca todo en enfoque de Entrenamiento(trainer) 

3. Verificar que estén actualizados:

  ° Instalar Ultralytics
  ° Instalar Numpy
  ° Instalar Flask
  ° Instalar Opencv-python (cv2)
  
    Alternativa 1
    -> pip install -r requirements.txt
    Alternativa 2
    -> pip install Ultralytics flask opencv-python numpy

  ° Verificar que el archivo del modelo (.pt) exista.
  ° Ejecutar el archivo app.py o index.py

    -> python app.py

# Creditos:
  Carlos Steven Cardenas
