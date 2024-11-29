# **WindMetric: Wind Speed Prediction App**

WindMetric is a comprehensive solution designed for predicting wind speed using a time series approach and machine learning models. The system is built using a **FastAPI** backend that hosts trained models, and a **Flutter** mobile application that allows users to input data and receive real-time predictions.

---

## **Project Overview**

### **1. Machine Learning Models**
- **Linear Regression**, **Decision Tree**, and **Random Forest** models were trained using historical weather data.
- The models utilize lagged features for wind speed, precipitation, temperature, and encoded weather conditions to predict future wind speeds.
- Best model selection based on **Mean Squared Error (MSE)**.

### **2. FastAPI Backend**
- Serves the trained model via a RESTful API for prediction requests.
- Includes a **Swagger UI** for interactive API documentation and testing.
- Input validation ensures reliable predictions.

### **3. Flutter Frontend**
- A clean, responsive user interface for interacting with the API.
- Users can enter lagged weather data and view wind speed predictions.
- Error handling for invalid or incomplete inputs.

---

## **Key Features**

### **FastAPI API**
- **Endpoint**: `/predict/` (POST request)
- **Input**: JSON payload containing:
  - `lag_wind_1`: Lagged wind speed in m/s.
  - `lag_precipitation_1`: Lagged precipitation in mm.
  - `lag_temp_max_1`: Lagged max temperature in °C.
  - `lag_temp_min_1`: Lagged min temperature in °C.
  - `weather_encoded`: Encoded weather condition (0-3).
- **Output**: Predicted wind speed in m/s.

### **Flutter Mobile App**
- Dynamic input fields for weather parameters.
- "Predict" button triggers API call to fetch predictions.
- Displays predicted wind speed or error messages.

---

## **Dataset**

- The dataset includes:
  - **Date**: Historical date.
  - **Wind speed**: Measured in meters per second (m/s).
  - **Precipitation**: Measured in millimeters (mm).
  - **Temperature**: Minimum and maximum temperatures in °C.
  - **Weather**: Encoded categories based on weather conditions.

### **Dataset Source**
- The dataset is sourced from a **[Seattle Weather Dataset](https://www.kaggle.com/code/petalme/seattle-weather-prediction/input)** hosted on a Kaggle for time series forecasting.

---

## **Setup and Deployment**

### **Backend (FastAPI)**
1. **Clone Repository**:
   ```bash
   git clone [https://github.com/dntwaritag/linear_regression_model.git](https://github.com/dntwaritag/linear_regression_model.git)
   cd linear_regression_model.git/API
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run API**:
   ```bash
   uvicorn prediction:app --host 0.0.0.0 --port 8000
   ```
4. Access the API at `http://127.0.0.1:8000/docs` for Swagger UI.

### **Frontend (Flutter)**
1. **Navigate to Flutter Project**:
   ```bash
   cd linear_regression_model.git/FlutterApp
   ```
2. **Install Dependencies**:
   ```bash
   flutter pub get
   ```
3. **Update API URL** in `main.dart`:
   ```dart
   final String apiUrl = '[https://your-api-url/predict/](https://linear-regression-model-sseb.onrender.com)';
   ```
4. **Run the App**:
   ```bash
   flutter run
   ```

---

## **Deployment**

### **API Hosting**
- Deployed via Render or similar service at:  
  **[Swagger UI URL Link](https://linear-regression-model-sseb.onrender.com)**

### **Flutter App Deployment**
- Can be tested on both physical and virtual devices.
- Supports iOS and Android platforms.

---

## **Model Training & Evaluation**

### **Model Comparison (MSE)**
- **Linear Regression**: `MSE = X.XX`
- **Decision Tree**: `MSE = Y.YY`
- **Random Forest**: `MSE = Z.ZZ`
- The **Linear Regression** model achieved the lowest MSE, making it the best-performing model.

---

## **Results**
- **High-accuracy predictions** based on real-time data input.
- Robust input validation ensures reliability.
- User-friendly mobile experience for wind speed forecasting.

---

## **Contact**
For any inquiries or support, reach out:  
**Name**: Denys Ntwaritaganzwa  
**Email**: [d.ntwaritag@alustudent.com](mailto:d.ntwaritag@alustudent.com)  
