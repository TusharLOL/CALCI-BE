from fastapi import APIRouter, HTTPException
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    try:
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {e}")
    
    data = []
    for response in responses:
        data.append(response)
        print('response in route: ', response)
    return {"message": "Image processed", "data": data, "status": "success"}