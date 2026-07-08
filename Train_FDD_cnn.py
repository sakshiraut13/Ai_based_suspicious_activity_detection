def main():
    import numpy as np
    import os
    from PIL import Image
    from sklearn.model_selection import train_test_split
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, Flatten, Dense
    from tensorflow.keras.utils import to_categorical
    from sklearn.utils import shuffle

    img_cols, img_rows = 64, 64

    # Function to load images from a directory
    def load_images_from_directory(directory):
        images = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                image_path = os.path.join(root, file)
                img = Image.open(image_path).convert('L').resize((img_cols, img_rows))
                images.append(np.array(img).flatten())
        return images

    # Load images for abnormal (fall) class
    abnormal_images = load_images_from_directory("D:/100% code suspicious/0")
    abnormal_labels = np.ones(len(abnormal_images))

    # Load images for normal (not fall) class
    normal_images = load_images_from_directory("D:/100% code suspicious/1")
    normal_labels = np.zeros(len(normal_images))

    # Combine images and labels
    images = np.vstack((abnormal_images, normal_images))
    labels = np.hstack((abnormal_labels, normal_labels))

    # Shuffle the data
    images, labels = shuffle(images, labels, random_state=2)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=1)

    # Reshape and normalize the data
    X_train = X_train.reshape(X_train.shape[0], img_cols, img_rows, 1).astype('float32') / 255
    X_test = X_test.reshape(X_test.shape[0], img_cols, img_rows, 1).astype('float32') / 255

    # Convert labels to one-hot encoding
    y_train = to_categorical(y_train, num_classes=2)
    y_test = to_categorical(y_test, num_classes=2)

    # Define the CNN model
    model = Sequential([
        Conv2D(64, kernel_size=3, activation='relu', input_shape=(img_cols, img_rows, 1)),
        Conv2D(32, kernel_size=3, activation='relu'),
        Flatten(),
        Dense(2, activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)

    # Evaluate the model
    _, accuracy = model.evaluate(X_test, y_test)
    print("Test Accuracy:", accuracy)

    # Save the model
    model.save("model.h5")

if __name__ == "__main__":
    main()