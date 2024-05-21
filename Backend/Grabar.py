from moviepy.editor import *
from PIL import ImageGrab
import numpy as np
import cv2

def grabarPantalla():
    while True:
        img = ImageGrab.grab (bbox=(0,0,320,224))
        np_img = np.array(img)
        cvt_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2BGR555)
        cv2.imshow("Grabacion", np_img)
        key=cv2.waitKey
        if key == 27:
            break
    cv2.destroyAllWindows
    
<<<<<<< HEAD
def crearClip():
    video = VideoFileClip("falta.avi")
    cortado = video.subclip(11, 15)
    cortado.write_videofile("clip.avi")
=======
def crearClip(file_in,file_out):
    cap = cv2.VideoCapture(file_in)

    # Verificar si el video está abierto
    if not cap.isOpened():
        print("No se pudo abrir el archivo de video.")
        return

    # Obtener la duración del video (en segundos)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # Definir la duración máxima deseada (en segundos)
    max_duration = 15

    if duration > max_duration:
        # Recortar el video a la duración máxima deseada
        frame_limit = int(max_duration * fps)
        cap.set(cv2.CAP_PROP_FRAME_COUNT, frame_limit)

    # Crear el objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(file_out, fourcc, fps, (320, 224))

    # Leer y escribir los fotogramas del video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (320, 224))
        out.write(frame)

    # Liberar los objetos VideoCapture y VideoWriter
    cap.release()
    out.release()

    print(f"El video se ha procesado correctamente y se ha guardado como '{file_out}'.")

crearClip("screen_recording.avi","clip.avi")
>>>>>>> f9af9f844a05c17f0575dde6e6c5a682e54b9c29
