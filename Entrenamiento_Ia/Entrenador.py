import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras

# Define hyperparameters
IMG_SIZE = 224 
BATCH_SIZE = 64
EPOCHS = 10

MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048

# Data preparation
train_df = pd.read_csv(r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\train.csv")
test_df = pd.read_csv(r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\test.csv")

def assign_label(tag):
    if tag == "falta":
        return 1
    elif tag == "No_falta":
        return 2
    else:
        return 0

train_df["label"] = train_df["tag"].apply(assign_label)
test_df["label"] = test_df["tag"].apply(assign_label)

# Define the model
def build_sequence_model():
    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")

    x = keras.layers.GRU(16, return_sequences=True)(
        frame_features_input, mask=mask_input
    )
    x = keras.layers.GRU(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(6, activation="softmax")(x)  # 6 clases: 5 tipos de falta y no falta

    sequence_model = keras.Model([frame_features_input, mask_input], output)

    sequence_model.compile(
        loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    return sequence_model

# Data preparation
def prepare_all_videos(df, root_dir):
    num_samples = len(df)
    video_paths = df["video_name"].values.tolist()
    labels = df["label"].values

    frame_masks = np.zeros(shape=(num_samples, MAX_SEQ_LENGTH), dtype="bool")
    frame_features = np.zeros(
        shape=(num_samples, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32"
    )

    for idx, path in enumerate(video_paths):
        frames = load_video(os.path.join(root_dir, path))
        frames = frames[None, ...]

        temp_frame_mask = np.zeros(
            shape=(
                1,
                MAX_SEQ_LENGTH,
            ),
            dtype="bool",
        )
        temp_frame_features = np.zeros(
            shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32"
        )

        for i, batch in enumerate(frames):
            video_length = batch.shape[0]
            length = min(MAX_SEQ_LENGTH, video_length)
            for j in range(length):
                temp_frame_features[i, j, :] = feature_extractor.predict(
                    batch[None, j, :], verbose=0,
                )
            temp_frame_mask[i, :length] = 1 

        frame_features[idx,] = temp_frame_features.squeeze()
        frame_masks[idx,] = temp_frame_mask.squeeze()

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

# Train the model
# train_data, train_labels = prepare_all_videos(train_df, r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\fault-detector-whit-IA\Dataset")
test_data, test_labels = prepare_all_videos(test_df, r"C:\Users\Javi_\OneDrive\Documentos\Proyecto_Final\fault-detector-whit-IA\Dataset")

# sequence_model = build_sequence_model()
# history = sequence_model.fit(
#     [train_data[0], train_data[1]],
#     train_labels,
#     validation_split=0.3,
#     epochs=EPOCHS,
#     batch_size=BATCH_SIZE
# )

# sequence_model.save("Detector_Faltas.keras")

sequence_model = keras.models.load_model("Detector_Faltas.keras")

# Evaluate the model
test_loss, test_accuracy = sequence_model.evaluate([test_data[0], test_data[1]], test_labels)
print(f"Test accuracy: {test_accuracy * 100}%")
