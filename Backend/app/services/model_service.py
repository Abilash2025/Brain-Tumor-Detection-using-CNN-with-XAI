import tensorflow as tf
import numpy as np

# Load trained model
model = tf.keras.models.load_model(
    "saved_models/brain_tumor_cnn.keras"
)

def predict(image_batch):

    predictions = model.predict(
        image_batch,
        verbose=0
    )

    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    )

    return {
        "predicted_class": predicted_class,
        "confidence": round(confidence * 100, 2)
    }

# Force graph initialization
dummy_input = tf.random.normal(
    (1, 224, 224, 3)
)

_ = model(dummy_input)
# Class names
class_names = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary"
]