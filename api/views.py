import numpy as np
import pandas as pd
import joblib
import os
from pathlib import Path

from django.shortcuts import render
from pages.models import Responses
from tensorflow.keras.models import load_model
from pages.preprocessing import preprocess_data


# --- Paths to model and preprocessing artifacts ---
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "api" / "model" / "vaccine_hesitancy_model.keras"
SCALER_PATH = BASE_DIR / "api" / "model" / "scaler.pkl"
FEATURE_ORDER_PATH = BASE_DIR / "api" / "model" / "feature_order.pkl"

# --- Load the trained Keras model ---
print("🔄 Loading model...")
try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
    print("📌 Model Input Shape:", model.input_shape)
except Exception as e:
    print("❌ Error loading model:", str(e))


def predict_hesitancy(request):
    """
    Predict vaccine hesitancy based on the latest submitted survey.
    """

    print("📩 Received request for prediction.")

    # Step 1: Get last user ID from session
    last_user_id = request.session.get('last_user_id')
    if not last_user_id:
        print("❌ No user ID found in session!")
        return render(request, "pages/error.html", {"message": "No survey data found!"})

    # Step 2: Fetch the response record from DB
    last_response = Responses.objects.filter(user_id=last_user_id).first()
    if not last_response:
        print("❌ No survey data found!")
        return render(request, "pages/error.html", {"message": "No survey data found!"})

    print("✅ Retrieved last survey response from database.")

    # Step 3: Extract user demographic + survey answers
    try:
        user_response = {
            "age": last_response.user_id.age,
            "sex": last_response.user_id.sex,
            "marital_status": last_response.user_id.marital_status,
            "no_of_children": last_response.user_id.no_of_children,
            "place": last_response.user_id.place,
            "qualification": last_response.user_id.qualification,
            "job": last_response.user_id.job,
        }
        for i in range(1, 31):
            user_response[f"question{i}"] = getattr(last_response, f"question{i}", None)

        print("✅ Extracted user response.")
    except AttributeError as e:
        print("❌ Error extracting user data:", str(e))
        return render(request, "pages/error.html", {"message": "User data extraction failed."})

    # Step 4: Convert to DataFrame
    response_df = pd.DataFrame([user_response])
    print("📌 DataFrame Shape:", response_df.shape)

    # Step 5: Preprocess input
    try:
        processed_input = preprocess_data(response_df)
        print("✅ Preprocessing successful!")
    except Exception as e:
        print("❌ Preprocessing error:", str(e))
        return render(request, "pages/error.html", {"message": f"Preprocessing error: {str(e)}"})

    # Step 6: Load expected feature order
    try:
        feature_order = joblib.load(FEATURE_ORDER_PATH)
        print("✅ Loaded trained feature order.")
    except Exception as e:
        print("❌ Error loading feature order:", str(e))
        return render(request, "pages/error.html", {"message": "Error loading feature order!"})

    # Step 7: Verify matching dimensions
    if len(feature_order) != processed_input.shape[1]:
        print("❌ Feature order mismatch!")
        return render(request, "pages/error.html", {"message": "Feature order mismatch after preprocessing!"})

    # Step 8: Reorder columns and convert to NumPy
    processed_input = processed_input.to_numpy()[:, feature_order]
    print("📌 Reordered Input Shape:", processed_input.shape)

    # Step 9: Load and apply scaler
    try:
        scaler = joblib.load(SCALER_PATH)
        print("✅ Scaler loaded.")
    except Exception as e:
        print("❌ Error loading scaler:", str(e))
        return render(request, "pages/error.html", {"message": "Error loading scaler!"})

    # Step 10: Scale the input
    processed_input = scaler.transform(processed_input).reshape(1, -1)
    print("📌 Final Processed Input Shape:", processed_input.shape)

    # Step 11: Run prediction
    try:
        prediction = model.predict(processed_input)
        predicted_class = np.argmax(prediction[0])
        hesitancy_score = round(float(np.max(prediction[0])) * 100, 2)

        hesitancy_labels = ['High Hesitancy', 'Low Hesitancy', 'Moderate Hesitancy']
        hesitancy_result = hesitancy_labels[predicted_class]

        # Step 12: Save to DB
        last_response.hesitancy_result = hesitancy_result
        last_response.hesitancy_score = hesitancy_score
        last_response.save()

        print(f"✅ Prediction saved: {hesitancy_result} ({hesitancy_score:.2f}%)")

    except Exception as e:
        print("❌ Model prediction error:", str(e))
        return render(request, "pages/error.html", {"message": f"Model prediction error: {str(e)}"})

    # Step 13: Return result to frontend
    return render(request, "pages/result.html", {
        "result": hesitancy_result,
    })
