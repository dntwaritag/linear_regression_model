import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const WindMetricApp());
}

class WindMetricApp extends StatelessWidget {
  const WindMetricApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WindMetric',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const WindPredictionPage(),
    );
  }
}

class WindPredictionPage extends StatefulWidget {
  const WindPredictionPage({Key? key}) : super(key: key);

  @override
  _WindPredictionPageState createState() => _WindPredictionPageState();
}

class _WindPredictionPageState extends State<WindPredictionPage> {
  // Controllers for input fields
  final TextEditingController lagWindController = TextEditingController();
  final TextEditingController lagPrecipController = TextEditingController();
  final TextEditingController lagTempMaxController = TextEditingController();
  final TextEditingController lagTempMinController = TextEditingController();
  final TextEditingController weatherEncodedController =
      TextEditingController();

  String _prediction = '';
  String _errorMessage = '';

  // API endpoint URL
  final String apiUrl =
      "https://linear-regression-model-sseb.onrender.com/predict/";

  // Make API request and get prediction
  Future<void> _predictWindSpeed() async {
    // Read input values
    final double lagWind = double.tryParse(lagWindController.text) ?? 0.0;
    final double lagPrecip = double.tryParse(lagPrecipController.text) ?? 0.0;
    final double lagTempMax = double.tryParse(lagTempMaxController.text) ?? 0.0;
    final double lagTempMin = double.tryParse(lagTempMinController.text) ?? 0.0;
    final int weatherEncoded = int.tryParse(weatherEncodedController.text) ?? 0;

    // Check for empty fields
    if (lagWind == 0.0 ||
        lagPrecip == 0.0 ||
        lagTempMax == 0.0 ||
        lagTempMin == 0.0 ||
        weatherEncoded == 0) {
      setState(() {
        _errorMessage = "Please fill in all fields with valid values.";
        _prediction = '';
      });
      return;
    }

    // Prepare data to send
    final Map<String, dynamic> inputData = {
      'lag_wind_1': lagWind,
      'lag_precipitation_1': lagPrecip,
      'lag_temp_max_1': lagTempMax,
      'lag_temp_min_1': lagTempMin,
      'weather_encoded': weatherEncoded
    };

    // Send POST request to API
    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: json.encode(inputData),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        setState(() {
          _prediction =
              "Predicted Wind Speed: ${data['predicted_wind_speed_m_s']} m/s";
          _errorMessage = '';
        });
      } else {
        setState(() {
          _errorMessage = "Error: ${response.body}";
          _prediction = '';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = "Error: $e";
        _prediction = '';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("WindMetric - Wind Speed Prediction"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Image (wind.jpeg)
            Image.asset('assets/wind.jpeg', height: 150), // My image file
            const SizedBox(height: 20),

            // Input fields
            TextField(
              controller: lagWindController,
              keyboardType: TextInputType.number,
              decoration:
                  const InputDecoration(labelText: 'Lagged Wind Speed (m/s)'),
            ),
            TextField(
              controller: lagPrecipController,
              keyboardType: TextInputType.number,
              decoration:
                  const InputDecoration(labelText: 'Lagged Precipitation (mm)'),
            ),
            TextField(
              controller: lagTempMaxController,
              keyboardType: TextInputType.number,
              decoration:
                  const InputDecoration(labelText: 'Lagged Max Temp (°C)'),
            ),
            TextField(
              controller: lagTempMinController,
              keyboardType: TextInputType.number,
              decoration:
                  const InputDecoration(labelText: 'Lagged Min Temp (°C)'),
            ),
            TextField(
              controller: weatherEncodedController,
              keyboardType: TextInputType.number,
              decoration:
                  const InputDecoration(labelText: 'Encoded Weather (0-3)'),
            ),

            const SizedBox(height: 20),

            // Predict Button
            ElevatedButton(
              onPressed: _predictWindSpeed,
              child: const Text("Predict"),
            ),

            const SizedBox(height: 20),

            // Display result or error message
            if (_prediction.isNotEmpty)
              Text(_prediction,
                  style: const TextStyle(
                      fontSize: 20, fontWeight: FontWeight.bold)),
            if (_errorMessage.isNotEmpty)
              Text(_errorMessage,
                  style: const TextStyle(fontSize: 16, color: Colors.red)),
          ],
        ),
      ),
    );
  }
}
