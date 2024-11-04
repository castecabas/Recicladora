import cv2

 #NOTE: todo lo relacionado con obtener las camaras(si hay),seleccionarla y cambiarla en el cv2. 

class Camera:
    def __init__(self):
        self.cameras = self._get_available_cameras()
        self.current_camera = 0 if self.cameras else None
        self.cap = cv2.VideoCapture(self.current_camera) if self.current_camera is not None else None

    def _get_available_cameras(self):
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def get_camera_list(self):
        return self.cameras

    def select_camera(self, camera_id):
        if camera_id in self.cameras:
            if self.cap is not None:
                self.cap.release()
            self.current_camera = camera_id
            self.cap = cv2.VideoCapture(self.current_camera)

    def get_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None