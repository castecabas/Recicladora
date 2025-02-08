import cv2

class Camera:
    def __init__(self):
        """ Inicializa la detección de cámaras disponibles y abre la primera cámara si está disponible. """
        self.cameras = self._get_available_cameras()
        self.current_camera = self.cameras[0] if self.cameras else None
        self.cap = cv2.VideoCapture(self.current_camera) if self.current_camera is not None else None

    def _get_available_cameras(self):
        """ Busca cámaras disponibles escaneando los primeros índices. """
        available_cameras = []
        for i in range(5):  # Reducimos a 5 para evitar tiempos largos de escaneo innecesario
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Evita retardos en Windows
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def get_camera_list(self):
        """ Devuelve la lista de cámaras disponibles. """
        return self.cameras

    def select_camera(self, camera_id):
        """ Cambia la cámara activa si es válida. """
        if camera_id in self.cameras:
            if self.cap is not None:
                self.cap.release()
            self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            if self.cap.isOpened():
                self.current_camera = camera_id
            else:
                print(f"Error: No se pudo abrir la cámara {camera_id}")
                self.cap = None

    def get_frame(self):
        """ Captura un frame de la cámara activa. """
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        """ Libera la cámara al salir. """
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __del__(self):
        """ Asegura que la cámara se libere cuando el objeto se destruya. """
        self.release()
