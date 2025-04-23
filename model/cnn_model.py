import tensorflow as tf
from tensorflow.keras import layers, models

def create_model(input_shape=(224, 224, 3), num_classes=2):
    """
    Create a CNN model for medical image analysis
    Args:
        input_shape: Tuple of input image dimensions (height, width, channels)
        num_classes: Number of output classes
    Returns:
        Compiled Keras model
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def preprocess_image(image):
    """
    Preprocess image for model input
    Args:
        image: Input image
    Returns:
        Preprocessed image
    """
    # Resize image to expected input shape
    image = tf.image.resize(image, [224, 224])
    # Normalize pixel values
    image = image / 255.0
    return image