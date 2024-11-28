import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Initialize FastAPI app
app = FastAPI(title="Wind Speed Prediction API", description="API for predicting wind speed using a Linear Regression model.")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a list of allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to the model and encoder
MODEL_PATH = 'best_timeseries_model.pkl'
LABEL_ENCODER_PATH = 'label_encoder.pkl'

# Load the trained model
try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
except Exception as e:
    raise ValueError(f"Error loading model or encoder: {e}")

# Input data schema for prediction
class PredictionInput(BaseModel):
    lag_wind_1: float = Field(..., gt=0, description="Lagged wind speed (previous day's wind speed) in m/s.")
    lag_precipitation_1: float = Field(..., ge=0, description="Lagged precipitation in mm.")
    lag_temp_max_1: float = Field(..., ge=-50, le=60, description="Lagged maximum temperature in °C (must be realistic).")
    lag_temp_min_1: float = Field(..., ge=-50, le=60, description="Lagged minimum temperature in °C.")
    weather_encoded: int = Field(..., ge=0, le=3, description="Weather encoded category (0 to 3).")

# Root route to redirect to Swagger UI
@app.get("/", summary="Root Endpoint")
def redirect_to_docs():
    """
    Redirect root to Swagger UI.
    """
    return RedirectResponse(url="/docs")

@app.post("/predict/", summary="Predict Wind Speed")
async def predict(input_data: PredictionInput):
    """
    Predict wind speed based on input features.
    """
    try:
        # Convert input data to numpy array for prediction
        input_array = np.array([[
            input_data.lag_wind_1,
            input_data.lag_precipitation_1,
            input_data.lag_temp_max_1,
            input_data.lag_temp_min_1,
            input_data.weather_encoded
        ]])

        # Predict using the loaded model
        prediction = model.predict(input_array)[0]

        # Return prediction 
        return {"predicted_wind_speed_m_s": round(prediction, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
