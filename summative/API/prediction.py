from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression  
from sklearn.preprocessing import LabelEncoder 

# Load your Linear Regression model
model = joblib.load('best_timeseries_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

app = FastAPI(title="Wind Speed Prediction API", description="API for predicting wind speed using a Linear Regression model.")

# Allow CORS for all origins (you can limit it to specific domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a list of allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class PredictionInput(BaseModel):
    lag_wind_1: float = Field(..., gt=0, description="Lagged wind speed (previous day's wind speed) in m/s.")
    lag_precipitation_1: float = Field(..., ge=0, description="Lagged precipitation in mm.")
    lag_temp_max_1: float = Field(..., ge=-50, le=60, description="Lagged maximum temperature in °C (must be realistic).")
    lag_temp_min_1: float = Field(..., ge=-50, le=60, description="Lagged minimum temperature in °C.")
    weather_encoded: int = Field(..., ge=0, le=3, description="Weather encoded category (0 to 3).")

@app.post("/predict", summary="Predict Wind Speed")
def predict(input_data: PredictionInput):
    # Convert input data to numpy array for prediction
    input_array = np.array([[input_data.lag_wind_1, input_data.lag_precipitation_1, input_data.lag_temp_max_1, input_data.lag_temp_min_1, input_data.weather_encoded]])
    
    try:
        prediction = model.predict(input_array)[0]
        return {"predicted_wind_speed_m_s": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
