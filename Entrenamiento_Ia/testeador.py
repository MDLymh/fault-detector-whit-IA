import os
import cv2
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input

# Define hyperparameters
IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 10

MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048

# Data preparation
train_df = pd.read_csv(r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\fault-detector-whit-IA\Entrenamiento_Ia\train.csv")
test_df = pd.read_csv(r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\fault-detector-whit-IA\Entrenamiento_Ia\test.csv")

def assign_label(tag):
    if tag == "falta":
        return 1
    elif tag == "No_falta":
        return 0
    else:
        return 0

train_df["label"] = train_df["tag"].apply(assign_label)
test_df["label"] = test_df["tag"].apply(assign_label)

# Load the feature extractor model
feature_extractor = ResNet50(weights="imagenet", include_top=False, pooling="avg", input_shape=(IMG_SIZE, IMG_SIZE, 3))

# Define the sequence model
def build_sequence_model():
    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")

    x = keras.layers.GRU(16, return_sequences=True)(frame_features_input, mask=mask_input)
    x = keras.layers.GRU(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(2, activation="softmax")(x)  # 2 clases: falta y no falta

    sequence_model = keras.Model([frame_features_input, mask_input], output)

    sequence_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return sequence_model

# Data preparation
def prepare_all_videos(df, root_dir):
    num_samples = len(df)
    video_paths = df["video_name"].values.tolist()
    labels = df["label"].values

    frame_masks = np.zeros(shape=(num_samples, MAX_SEQ_LENGTH), dtype="bool")
    frame_features = np.zeros(shape=(num_samples, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for idx, path in enumerate(video_paths):
        frames = load_video(os.path.join(root_dir, path))
        frames = frames[None, ...]

        temp_frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH), dtype="bool")
        temp_frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

        for i, batch in enumerate(frames):
            video_length = batch.shape[0]
            length = min(MAX_SEQ_LENGTH, video_length)
            for j in range(length):
                img = preprocess_input(batch[j])
                temp_frame_features[i, j, :] = feature_extractor.predict(img[None, :, :, :], verbose=0)
            temp_frame_mask[i, :length] = 1

        frame_features[idx, ] = temp_frame_features.squeeze()
        frame_masks[idx, ] = temp_frame_mask.squeeze()

    return (frame_features, frame_masks), labels

# Load a video from a local file
def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)

def crop_center_square(frame):
    y, x, _ = frame.shape
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

# Function to predict a new video
def predict_new_video_with_percentage(video_path, model):
    frames = load_video(video_path)
    frames = frames[None, ...]

    temp_frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH), dtype="bool")
    temp_frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            img = preprocess_input(batch[j])
            temp_frame_features[i, j, :] = feature_extractor.predict(img[None, :, :, :], verbose=0)
        temp_frame_mask[i, :length] = 1

    prediction = model.predict([temp_frame_features, temp_frame_mask])
    probabilities = prediction[0] * 100  # Escala las probabilidades a 0-100%
    predicted_label = np.argmax(prediction, axis=1)[0]

    if predicted_label == 1:
        print("Predicción: Falta")
    else:
        print("Predicción: No falta")

    print(f"Probabilidad de falta: {probabilities[1]:.2f}%")
    print(f"Probabilidad de no falta: {probabilities[0]:.2f}%")

# Load the model
model_path = r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\fault-detector-whit-IA\Entrenamiento_Ia\Detector_Faltas.keras"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"El archivo {model_path} no se encontró.")
sequence_model = keras.models.load_model(model_path)

# Predict on a new video
new_video_path = r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\pruebas\prueba"  # Asegúrate de que esta sea una ruta de archivo de video válida
predict_new_video_with_percentage(new_video_path, sequence_model)
