import tensorflow as tf
import numpy as np
import cv2
import matplotlib.cm as cm

IMAGE_SIZE = 224

def generate_gradcam(
    image_batch,
    model,
    last_conv_layer_name="last_conv_layer"
):

    # Get last conv layer
    last_conv_layer = model.get_layer(
        last_conv_layer_name
    )

    # Create feature extractor
    last_conv_layer_model = tf.keras.Model(
        model.inputs,
        last_conv_layer.output
    )

    # Create classifier model
    classifier_input = tf.keras.Input(
        shape=last_conv_layer.output.shape[1:]
    )

    x = classifier_input

    # Rebuild classifier head manually
    start = False

    for layer in model.layers:

        if start:
            x = layer(x)

        if layer.name == last_conv_layer_name:
            start = True

    classifier_model = tf.keras.Model(
        classifier_input,
        x
    )

    # Compute Grad-CAM
    with tf.GradientTape() as tape:

        # Get conv outputs
        conv_outputs = last_conv_layer_model(
            image_batch
        )

        tape.watch(conv_outputs)

        # Get predictions
        predictions = classifier_model(
            conv_outputs
        )

        predicted_index = tf.argmax(
            predictions[0]
        )

        class_channel = predictions[
            :,
            predicted_index
        ]

    # Compute gradients
    gradients = tape.gradient(
        class_channel,
        conv_outputs
    )

    # Global average pooling
    pooled_gradients = tf.reduce_mean(
        gradients,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_gradients[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    # Apply ReLU
    heatmap = tf.maximum(
        heatmap,
        0
    )

    # Normalize
    heatmap = heatmap / tf.math.reduce_max(
        heatmap
    )

    return heatmap.numpy()

def create_overlay(
    original_image,
    heatmap
):

    # Resize heatmap
    heatmap = cv2.resize(
        heatmap,
        (IMAGE_SIZE, IMAGE_SIZE)
    )

    # Convert heatmap to RGB
    heatmap_colored = cm.jet(
        heatmap
    )[:, :, :3]

    # Normalize original image
    original_image = original_image / 255.0

    # Create overlay
    overlay = (
        heatmap_colored * 0.4 +
        original_image
    )

    # Clip values
    overlay = np.clip(
        overlay,
        0,
        1
    )

    return overlay