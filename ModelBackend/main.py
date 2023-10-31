
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Load the "keratoconusdetect" model
keratoconus_model = load_model('keratoconus.h5')

# Define the target image size expected by the model
target_size = (224, 224)


@app.route('/predict_keratoconus', methods=['POST'])
def predict_keratoconus():
    try:
        # Get the image file from the request
        image_file = request.files['image']

        # Read the image using OpenCV
        img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Resize the image to the target size (224x224) if needed
        if img.shape[:2] != target_size:
            img = cv2.resize(img, target_size)

        # Preprocess the image
        img = img / 255.0  # Normalize the image (if needed)
        img = np.expand_dims(img, axis=0)

        # Make predictions using the "keratoconusdetect" model
        predictions = keratoconus_model.predict(img)

        # Assuming your model has three classes: Normal, Keratoconus, and Suspect
        class_labels = ['Normal', 'Keratoconus', 'Suspect']

        # Get the class with the highest probability
        predicted_class = np.argmax(predictions)

        # Get the probability associated with the predicted class
        predicted_probability = predictions[0][predicted_class]

        # Define probability thresholds for different classes
        probability_thresholds = {
            'Normal': 0.7,  # Adjust this threshold as needed
            'Keratoconus': 0.5,  # Adjust this threshold as needed
            'Suspect': 0.3  # Adjust this threshold as needed
        }

        # Determine the class label based on the probability range
        predicted_label = None
        for label, threshold in probability_thresholds.items():
            if predicted_probability >= threshold:
                predicted_label = label
                break

        response = {
            "prediction": predicted_label,
            "probability": float(predicted_probability)
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
