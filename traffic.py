import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import sys
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input


IMG_HEIGHT = 30
IMG_WIDTH = 30
NUM_CATEGORIES = 43
EPOCHS = 10
BATCH_SIZE = 64

def load_data(data_dir):
    images = []
    labels = []

    for label in range(NUM_CATEGORIES):
        folder_path = os.path.join(data_dir, str(label))
        if not os.path.isdir(folder_path):
            continue

        for file_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file_name)
            image = cv2.imread(img_path)
            if image is None:
                continue  
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            images.append(image)
            labels.append(label)

    return np.array(images), np.array(labels)

def get_model():
    model = Sequential([
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(NUM_CATEGORIES, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    data_dir = sys.argv[1]

    print("Loading data...")
    images, labels = load_data(data_dir)
    print("Data loaded.")

    images = images.astype("float32") / 255.0

  
    labels = to_categorical(labels, NUM_CATEGORIES)

    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.4)

    model = get_model()

    print("Training model...")
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)

    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}")


    print("Evaluating model...")
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Model accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
