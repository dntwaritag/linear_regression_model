from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load model and supporting files
model = joblib.load('models/best_model.pkl')
scaler = joblib.load('models/scaler.pkl')
label_encoders = {
    "Area": joblib.load('models/label_encoder_area.pkl'),
    "Element": joblib.load('models/label_encoder_element.pkl'),
    "Item": joblib.load('models/label_encoder_item.pkl'),
    "Unit": joblib.load('models/label_encoder_unit.pkl'),
}

# Define input schema
class PredictionRequest(BaseModel):
    Area: str
    Element: Literal["Yield"]
    Item: str
    Year: int = Field(..., ge=1960, le=2025)
    Unit: str

# Define prediction endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    # Encode inputs
    inputs = [
        label_encoders["Area"].transform([request.Area])[0],
        label_encoders["Element"].transform([request.Element])[0],
        label_encoders["Item"].transform([request.Item])[0],
        request.Year,
        label_encoders["Unit"].transform([request.Unit])[0],
    ]

    # Scale inputs
    inputs_scaled = scaler.transform([inputs])

    # Predict
    prediction = model.predict(inputs_scaled)[0]

    return {"predicted_value": prediction}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
