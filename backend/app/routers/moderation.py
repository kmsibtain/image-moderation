from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from services.database import get_usages_collection
from models.token import Token
from models.usage import Usage
from utils.auth import get_current_token
from datetime import datetime
import io
from PIL import Image
from pymongo.collection import Collection
import asyncio
import numpy as np

router = APIRouter(tags=["Moderation"])

@router.post("/moderate")
async def moderate_image(
    file: UploadFile = File(...),
    current_token: Token = Depends(get_current_token),
    usages_collection: Collection = Depends(get_usages_collection)
):
    """
    Analyzes an uploaded image and returns a content-safety report.
    Requires any valid bearer token.
    """
    # Record API hit using executor for synchronous operation
    usage = Usage(token=current_token.token, endpoint="/moderate", timestamp=datetime.utcnow())
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: usages_collection.insert_one(usage.dict(by_alias=True))
    )

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only image files are allowed.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Convert image to RGB if it isn't already, to ensure consistent processing
        if image.mode != "RGB":
            image = image.convert("RGB")

        # --- Simulated Image Moderation Logic ---
        moderation_results = {
            "violence": {"detected": False, "confidence": 0.05},
            "nudity": {"detected": False, "confidence": 0.05},
            "hate_symbols": {"detected": False, "confidence": 0.05},
            "self_harm": {"detected": False, "confidence": 0.05},
            "extremist_propaganda": {"detected": False, "confidence": 0.05},
            "general_safety": "safe"
        }

        # Simulate a simple detection based on image properties
        if image.width > 2000 or image.height > 2000:
            moderation_results["general_safety"] = "potential_concern"
            moderation_results["violence"]["detected"] = True
            moderation_results["violence"]["confidence"] = 0.75

        # Additional manual moderation logic
        # 1. Check image brightness (simulating detection of overly dark images)
        image_array = np.array(image.convert("L"))  # Convert to grayscale for brightness analysis
        avg_brightness = np.mean(image_array)
        if avg_brightness < 50:  # Threshold for "dark" images (0-255 scale)
            moderation_results["general_safety"] = "potential_concern"
            moderation_results["self_harm"]["detected"] = True
            moderation_results["self_harm"]["confidence"] = 0.65

        # 2. Check for excessive red tones (simulating detection of gore)
        r, g, b = image.split()
        red_proportion = np.mean(np.array(r)) / (np.mean(np.array(g)) + np.mean(np.array(b)) + np.mean(np.array(r)) + 1e-10)
        if red_proportion > 0.5:  # If red dominates significantly
            moderation_results["general_safety"] = "potential_concern"
            moderation_results["violence"]["detected"] = True
            moderation_results["violence"]["confidence"] = max(moderation_results["violence"]["confidence"], 0.8)

        # 3. Check aspect ratio (simulating detection of narrow/wide images)
        aspect_ratio = image.width / image.height if image.height > 0 else 1
        if aspect_ratio > 3 or aspect_ratio < 0.33:  # Very wide or very tall images
            moderation_results["general_safety"] = "potential_concern"
            moderation_results["hate_symbols"]["detected"] = True
            moderation_results["hate_symbols"]["confidence"] = 0.6

        # 4. Check color saturation (simulating detection of manipulated content)
        image_array_rgb = np.array(image)
        r, g, b = image_array_rgb[:,:,0], image_array_rgb[:,:,1], image_array_rgb[:,:,2]
        max_channel = np.maximum(np.maximum(r, g), b)
        min_channel = np.minimum(np.minimum(r, g), b)
        saturation = np.mean((max_channel - min_channel) / (max_channel + 1e-10))  # Avoid division by zero
        if saturation > 0.7:  # Highly saturated images
            moderation_results["general_safety"] = "potential_concern"
            moderation_results["nudity"]["detected"] = True
            moderation_results["nudity"]["confidence"] = 0.7

        # 5. Simulate edge detection (simulating detection of text or symbols)
        image_gray = image.convert("L")
        image_array_gray = np.array(image_gray)
        if image_array_gray.shape[0] > 1 and image_array_gray.shape[1] > 1:  # Ensure image has enough dimensions
            row_diff = np.diff(image_array_gray, axis=0)  # Shape: (height-1, width)
            col_diff = np.diff(image_array_gray, axis=1)  # Shape: (height, width-1)
            row_diff_padded = np.pad(row_diff, ((0, 1), (0, 0)), mode='constant', constant_values=0)  # Match height
            col_diff_padded = np.pad(col_diff, ((0, 0), (0, 1)), mode='constant', constant_values=0)  # Match width
            edges = np.abs(row_diff_padded) + np.abs(col_diff_padded)
            edge_density = np.mean(edges > 10)  # Threshold for significant edges
            if edge_density > 0.1:  # High density of sharp edges
                moderation_results["general_safety"] = "potential_concern"
                moderation_results["hate_symbols"]["detected"] = True
                moderation_results["hate_symbols"]["confidence"] = max(moderation_results["hate_symbols"]["confidence"], 0.75)

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "moderation_report": moderation_results
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing image: {str(e)}")