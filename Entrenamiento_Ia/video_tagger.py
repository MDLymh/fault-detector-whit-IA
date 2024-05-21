import os
import csv

def extract_tag(filename):
    # Convertimos el nombre del archivo a minúsculas para una comparación uniforme
    lower_filename = filename.lower()
    if 'no falta' in lower_filename or 'nofalta' in lower_filename or 'no_falta' in lower_filename:
        return 'No Falta'
    elif 'falta' in lower_filename:
        return 'Falta'
    return 'Desconocido'

def process_videos(input_folder, train_csv, test_csv):
    # Listas para almacenar los datos de los videos
    train_videos_data = []
    test_videos_data = []

    # Recorremos todos los archivos en la carpeta dada
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.avi', '.mp4', '.mkv', '.mov')):  # Añade otras extensiones si es necesario
                # Extraemos el tag del nombre del archivo
                tag = extract_tag(file)
                # Formateamos la ruta como se requiere
                train_video_name = f'train/{file}'
                test_video_name = f'test/{file}'
                # Añadimos la información a las listas
                train_videos_data.append([train_video_name, tag])
                test_videos_data.append([test_video_name, tag])

    # Guardamos los datos en el archivo CSV para train
    with open(train_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribimos el encabezado
        csvwriter.writerow(['video_name', 'tag'])
        # Escribimos los datos de los videos
        csvwriter.writerows(train_videos_data)

    # Guardamos los datos en el archivo CSV para test
    with open(test_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribimos el encabezado
        csvwriter.writerow(['video_name', 'tag'])
        # Escribimos los datos de los videos
        csvwriter.writerows(test_videos_data)

# Especifica la carpeta de entrada y los archivos CSV de salida
input_folder = r'C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\fault-detector-whit-IA\Dataset'  # Reemplaza esto con la ruta a tu carpeta de videos
train_csv = 'train.csv'
test_csv = 'test.csv'

# Llamamos a la función para procesar los videos y generar los CSV
process_videos(input_folder, train_csv, test_csv)
