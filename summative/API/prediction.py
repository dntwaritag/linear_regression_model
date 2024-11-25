from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Load the model
model = joblib.load('best_model.pkl')

# Initialize the app
app = FastAPI(title="YieldVision API", description="API for Predicting Yield", version="1.0.0")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data schema using Pydantic
class PredictionInput(BaseModel):
    Area: int = Field(..., title="Area Code", ge=0)
    Element: int = Field(..., title="Element Code", ge=0)
    Item: int = Field(..., title="Item Code", ge=0)
    Unit: int = Field(..., title="Unit Code", ge=0)

@app.post("/predict", summary="Predict Yield")
async def predict(input_data: PredictionInput):
    # Convert input into numpy array
    input_array = np.array([input_data.Area, input_data.Element, input_data.Item, input_data.Unit]).reshape(1, -1)

    try:
        # Make prediction
        prediction = model.predict(input_array)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
