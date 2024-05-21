import os
from moviepy.editor import *

def convertir_a_avi(carpeta_src, carpeta_out):
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(carpeta_out):
        os.makedirs(carpeta_out)

    # Obtener la lista de archivos en la carpeta de origen
    archivos = os.listdir(carpeta_src)

    # Iterar sobre cada archivo en la carpeta de origen
    for archivo in archivos:
        # Verificar si el archivo es un video
        if archivo.endswith((".mp4", ".mov", ".mkv")):
            ruta_completa = os.path.join(carpeta_src, archivo)
            nombre_sin_extension = os.path.splitext(archivo)[0]
            archivo_salida = os.path.join(carpeta_out, nombre_sin_extension + ".avi")

            # Convertir el video a formato AVI sin audio
            video = VideoFileClip(ruta_completa)
            video_cortado = video.subclip(0, video.duration)
            video_cortado_resized = video_cortado.crop(x1=0, y1=0, x2=320, y2=224)
            video_cortado_resized.write_videofile(archivo_salida, codec='libx264', bitrate="500k", audio_codec='pcm_s16le', threads=4)
            video_cortado_resized.close()

            print(f"Se ha convertido {archivo} a AVI.")

# Obtener la ruta absoluta del directorio donde se encuentra el script
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Directorio de entrada (donde están los videos)
directorio_entrada = directorio_script

# Directorio de salida (donde se guardarán los videos convertidos)
directorio_salida = directorio_script

# Llamar a la función para convertir los videos
convertir_a_avi(directorio_entrada, directorio_salida)
