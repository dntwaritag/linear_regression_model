from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

class PredictionInput(BaseModel):
    area: float = Field(..., ge=0, le=10000, description="Area of land in hectares. Range: 0-10000")
    year: int = Field(..., ge=2000, le=2100, description="Year of prediction. Range: 2000-2100")
    element: str = Field(..., max_length=50, description="Element for prediction")
    item: str = Field(..., max_length=50, description="Item to be predicted")
    unit: str = Field(..., max_length=20, description="Unit of measurement for prediction")

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True

app = FastAPI()

# Allow CORS for all origins (you can restrict it to specific domains for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (adjust as needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Load your trained model (ensure you save your model as 'best_model.pkl')
model = joblib.load('best_model.pkl')
@app.post('/predict')

def predict(input_data: PredictionInput):
    # Convert the input data into a format suitable for prediction
    input_features = np.array([[input_data.area, input_data.year, input_data.element, input_data.item, input_data.unit]])

    # Make a prediction using the model
    prediction = model.predict(input_features)
    
    # Return the prediction result
    return {"prediction": prediction[0]}
