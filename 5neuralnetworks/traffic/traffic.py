import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import keras
from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    dir_path = os.path.normpath(data_dir)

    images = []
    labels = []
    for i in range(NUM_CATEGORIES):
        category_dir = os.path.join(dir_path, str(i))
        for filename in os.listdir(category_dir):
            image = cv2.imread(os.path.join(category_dir, filename))
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            images.append(image)
            labels.append(i)
    return (images, labels)


# def platform_independent_directory(data_dir):
#     """

#     """
#     path = os.path.normpath(data_dir)

#     path_list = []
#     if "\\" in path:
#         path_list = path.split("\\")
#         print(path_list)
#     else:
#         path_list = path.split("/")
#         path_list[0] = "/"
#         print(path_list)
#     return os.path.join(*path_list)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # create a functional model
    model = keras.models.Sequential(
        [
            # input layer
            keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
            # convolutional layer # 1 - convolution applies filters that can help the AI observe new things in the image, by changing the kernel.
            keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation="relu"),
            # pooling layer #1 - help capture low level image features (edges & lines) multiple pooling layers eventually "add up" to make more complex image features
            keras.layers.MaxPooling2D(pool_size=(2, 2)),
            # dropout layer #1 - prevents overfitting of data in the convolutional layers
            keras.layers.Dropout(rate=0.1),
            keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation="relu"),
            keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation="relu"),
            keras.layers.MaxPooling2D(pool_size=(2, 2)),
            keras.layers.Dropout(rate=0.1),
            # flattening removes output from convolutional layers and transforms them into a 1D vector allowing them to be fed to fully connected layers
            # fully connected layers handle all of the relationships learned from convolutional layers
            # flattening allows each neuron in the FCLs to consider everything learn from the convolutional layers simultaneously
            keras.layers.Flatten(),
            # fully connected dropout layer
            keras.layers.Dense(256, activation="relu"),
            keras.layers.Dropout(rate=0.1),
            # output layer
            keras.layers.Dense(43, activation="softmax"),
        ]
    )
    # model = keras.Model(inputs=inputs, outputs=output)
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    main()
