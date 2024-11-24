from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your allowed origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the saved model
model = joblib.load('best_model.pkl')

# Define the input schema using Pydantic
class PredictionInput(BaseModel):
    Area: int = Field(..., ge=0, description="Encoded Area category")
    Element: int = Field(..., ge=0, description="Encoded Element category")
    Item: int = Field(..., ge=0, description="Encoded Item category")
    Unit: int = Field(..., ge=0, description="Encoded Unit category")
    Year: int = Field(..., ge=1900, le=2100, description="Year of the observation")

# Define the prediction endpoint
@app.post("/predict")
def predict(input_data: PredictionInput):
    """
    Predict the value based on input features.
    """
    # Convert input to a NumPy array for prediction
    features = np.array([[input_data.Area, input_data.Element, input_data.Item, input_data.Unit, input_data.Year]])
    
    try:
        # Make prediction
        prediction = model.predict(features)
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
