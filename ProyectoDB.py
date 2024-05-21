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
    
def crearClip():
    video = VideoFileClip("falta.avi")
    cortado = video.subclip(11, 15)
    cortado.write_videofile("clip.avi")