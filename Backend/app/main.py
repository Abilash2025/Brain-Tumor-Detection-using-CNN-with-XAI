from fastapi import FastAPI, UploadFile, File

from app.services.model_service import (
    predict,
    model
)

from app.xai.gradcam import (
    generate_gradcam,
    create_overlay
)

from app.utils.image_processing import preprocess_image

from fastapi.staticfiles import StaticFiles

from PIL import Image

import numpy as np

import uuid

import matplotlib.pyplot as plt

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://brain-tumor-detection-using-cnn-wit.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

@app.get("/")
def home():

    return {
        "message": "Brain Tumor XAI API Running"
    }


@app.post("/predict")
async def predict_tumor(
    file: UploadFile = File(...)
):

    # Read image bytes
    image_bytes = await file.read()

    # Preprocess
    image_batch = preprocess_image(
        image_bytes
    )

    # Prediction
    result = predict(image_batch)

    # Generate heatmap
    heatmap = generate_gradcam(
        image_batch,
        model
    )

    # Original image for overlay
    image = Image.open(file.file)

    image = image.convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image)

    # Create overlay
    overlay = create_overlay(
        image_array,
        heatmap
    )

    # Save overlay image
    filename = f"{uuid.uuid4()}.png"

    filepath = f"static/{filename}"

    plt.imsave(filepath, overlay)

    # Add overlay URL
    result["gradcam_image"] = (
        f"/static/{filename}"
    )

    return result#test 
