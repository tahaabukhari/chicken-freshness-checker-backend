"""
analyzer.py — ML & Data Processing Service
============================================
This module is the single entry-point for all spoilage prediction logic.
It currently contains DUMMY logic that will be replaced with your trained
machine-learning model.

HOW TO INTEGRATE YOUR OWN ML MODEL
-----------------------------------
1. Place your trained model file (e.g., model.pkl, model.onnx) inside
   the `app/services/` directory (or any path you prefer).

2. Uncomment and adapt the import + loading block below.

3. Replace the body of `calculate_spoilage()` with a call to your model's
   `.predict()` method.

==========================================================================
"""

# =========================================================================
# >>>  STEP 1 — IMPORT YOUR ML LIBRARIES HERE  <<<
# =========================================================================
# Uncomment the libraries you need:
#
# import joblib                          # For scikit-learn .pkl models
# import onnxruntime as ort              # For ONNX models
# import numpy as np                     # Almost always needed
# import pandas as pd                    # If your model expects a DataFrame
#
# from pathlib import Path
# =========================================================================


# =========================================================================
# >>>  STEP 2 — LOAD YOUR MODEL HERE (runs once at import time)  <<<
# =========================================================================
# This block executes once when the module is first imported by FastAPI,
# so the model stays in memory for fast inference on every request.
#
# MODEL_PATH = Path(__file__).parent / "model.pkl"
# model = joblib.load(MODEL_PATH)
#
# --- OR for ONNX ---
# MODEL_PATH = Path(__file__).parent / "model.onnx"
# ort_session = ort.InferenceSession(str(MODEL_PATH))
# =========================================================================


def calculate_spoilage(
    temperature: float,
    humidity: float,
    gas_sensor: float,
) -> tuple[float, str]:
    """
    Analyze sensor readings and return a spoilage assessment.

    Parameters
    ----------
    temperature : float
        Temperature in °C from the IoT sensor.
    humidity : float
        Relative humidity (%) from the IoT sensor.
    gas_sensor : float
        Combined methane/ammonia gas reading (arbitrary units).

    Returns
    -------
    tuple[float, str]
        spoilage_percent : 0.0 – 100.0
        category         : "fresh" | "old-fresh" | "semi-spoiled" | "spoiled"

    =======================================================================
    >>>  STEP 3 — REPLACE THE DUMMY LOGIC BELOW WITH YOUR MODEL  <<<
    =======================================================================
    Example with a scikit-learn model:

        features = np.array([[temperature, humidity, gas_sensor]])
        spoilage_percent = float(model.predict(features)[0])

    Example with ONNX:

        input_name  = ort_session.get_inputs()[0].name
        features    = np.array([[temperature, humidity, gas_sensor]],
                               dtype=np.float32)
        prediction  = ort_session.run(None, {input_name: features})
        spoilage_percent = float(prediction[0][0])

    Then determine the category from spoilage_percent using your own
    thresholds (or let the model output it directly).
    =======================================================================
    """

    # ----- DUMMY LOGIC (replace me!) -----
    # Simple weighted heuristic for development/testing purposes.
    # Higher temp & gas readings → more spoilage.
    spoilage_percent = min(
        100.0,
        max(
            0.0,
            (temperature - 4.0) * 2.5   # deviation from ideal 4 °C
            + gas_sensor * 0.5           # gas contribution
            + (humidity - 50.0) * 0.3    # humidity contribution
        ),
    )

    # ----- CATEGORY THRESHOLDS (adjust to your training data) -----
    if spoilage_percent < 25.0:
        category = "fresh"
    elif spoilage_percent < 50.0:
        category = "old-fresh"
    elif spoilage_percent < 75.0:
        category = "semi-spoiled"
    else:
        category = "spoiled"

    return spoilage_percent, category
