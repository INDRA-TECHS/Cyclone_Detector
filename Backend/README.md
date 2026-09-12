# CycloCast Backend — Inference Gateway

**Prepared by:** Tisha Biswas

FastAPI backend serving as the inference gateway for the Cyclone Prediction Console dashboard.

## Endpoint
- `POST /predict-combined` — accepts a satellite image + numeric storm history JSON, returns image classification, track/intensity prediction, and threat level summary.

## How to run
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002
```

Then visit `http://127.0.0.1:8002/docs` to test interactively.

## Note
`mock_cnn_predict` and `predict_numerical` are currently rule-based placeholders (no trained model weights supplied yet). Replace with real CNN/XGBoost models when available.
