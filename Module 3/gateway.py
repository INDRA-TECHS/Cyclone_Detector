import json
import httpx
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cyclone Prediction Gateway")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_SERVICE_URL = "http://127.0.0.1:8000/predict"
NUMERIC_SERVICE_URL = "http://127.0.0.1:8001/predict"

DEFAULT_PAYLOAD = {
    "horizon": "+12h",
    "history": [
        {"ISO_TIME": "1985-10-10 18:00:00", "LAT": 9.1, "LON": 129.9, "WIND_KTS": 25, "PRES_MB": 1004, "STORM_SPEED": 9, "DIST2LAND": 395},
        {"ISO_TIME": "1985-10-11 00:00:00", "LAT": 9.2, "LON": 129.5, "WIND_KTS": 25, "PRES_MB": 1004, "STORM_SPEED": 9, "DIST2LAND": 311},
        {"ISO_TIME": "1985-10-11 06:00:00", "LAT": 9.7, "LON": 129.1, "WIND_KTS": 30, "PRES_MB": 1000, "STORM_SPEED": 10, "DIST2LAND": 280},
        {"ISO_TIME": "1985-10-11 12:00:00", "LAT": 10.1, "LON": 128.6, "WIND_KTS": 35, "PRES_MB": 998, "STORM_SPEED": 11, "DIST2LAND": 250},
        {"ISO_TIME": "1985-10-11 18:00:00", "LAT": 10.6, "LON": 128.0, "WIND_KTS": 40, "PRES_MB": 995, "STORM_SPEED": 12, "DIST2LAND": 210},
        {"ISO_TIME": "1985-10-12 00:00:00", "LAT": 11.2, "LON": 127.3, "WIND_KTS": 50, "PRES_MB": 990, "STORM_SPEED": 13, "DIST2LAND": 180}
    ]
}

DEFAULT_JSON_STR = json.dumps(DEFAULT_PAYLOAD)

@app.post("/predict-combined")
async def predict_combined(
    file: UploadFile = File(...),
    numeric_json: str = Form(default=DEFAULT_JSON_STR)
):
    try:
        numeric_payload = json.loads(numeric_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON string format: {str(e)}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Call Image Microservice
        file_bytes = await file.read()
        files = {"file": (file.filename, file_bytes, file.content_type)}
        try:
            img_res = await client.post(IMAGE_SERVICE_URL, files=files)
            img_res.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Image API Error: {str(e)}")

        # Call Numeric Microservice
        try:
            num_res = await client.post(
                NUMERIC_SERVICE_URL, 
                json=numeric_payload,
                headers={"Content-Type": "application/json"}
            )
            num_res.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Numeric API Error: {str(e)}")

    img_data = img_res.json()
    num_data = num_res.json()

    # Consolidated Decision Logic
    is_critical = num_data.get("intensification_warning", False) or "Severe" in img_data.get("prediction", "")

    return {
        "status": "success",
        "summary": {
            "overall_threat_level": "HIGH" if is_critical else "MODERATE",
            "predicted_coordinates": [num_data.get("predicted_lat"), num_data.get("predicted_lon")],
            "visual_classification": img_data.get("prediction"),
            "numerical_category": num_data.get("category")
        },
        "image_classification": img_data,
        "numerical_prediction": num_data
    }