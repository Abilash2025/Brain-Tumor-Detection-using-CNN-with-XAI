import tensorflow as tf

IMAGE_SIZE = 224

def preprocess_image(image_bytes):

    # Decode image
    image = tf.io.decode_jpeg(
        image_bytes,
        channels=3,
    )

    # Resize image
    image = tf.image.resize(
        image,
        [IMAGE_SIZE, IMAGE_SIZE]
    )

    # Convert to float32
    image = tf.cast(
        image,
        tf.float32
    )

    # Add batch dimension
    image = tf.expand_dims(
        image,
        axis=0
    )

    return image