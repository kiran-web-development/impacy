from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
import numpy as np
import cv2
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
import threading

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.image_utils import load_medical_image, enhance_image, segment_image
from model.cnn_model import create_model, preprocess_image

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize ThreadPoolExecutor for async processing
executor = ThreadPoolExecutor(max_workers=3)

# Initialize the model with threading lock
model = None
model_lock = threading.Lock()
UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_model():
    global model
    with model_lock:
        if model is None:
            model = create_model()
            # Load pre-trained weights if available
            weights_path = os.getenv('MODEL_PATH')
            if weights_path and os.path.exists(weights_path):
                model.load_weights(weights_path)
    return model

def process_image(image):
    """Process image in a separate thread"""
    enhanced = enhance_image(image)
    segmented = segment_image(enhanced)
    processed = preprocess_image(enhanced)
    return enhanced, segmented, processed

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "AI Medical Image Analysis System is running",
        "model_loaded": model is not None
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the uploaded file with a unique name
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, f"{os.urandom(8).hex()}_{filename}")
        file.save(filepath)

        # Load the image
        image = load_medical_image(filepath)
        if image is None:
            return jsonify({"error": "Failed to load image"}), 400

        # Process image asynchronously
        enhanced, segmented, processed = executor.submit(process_image, image).result()
        
        # Get model prediction
        model = get_model()
        if model:
            # Expand dimensions for batch processing
            batch = np.expand_dims(processed, axis=0)
            prediction = model.predict(batch, verbose=0)
            
            # Process prediction results
            confidence = float(np.max(prediction[0]))
            predicted_class = int(np.argmax(prediction[0]))
        else:
            confidence = 0.0
            predicted_class = -1

        # Return immediate response with analysis details
        response = {
            "status": "success",
            "message": "Image analyzed successfully",
            "details": {
                "dimensions": image.shape,
                "confidence_score": f"{confidence:.2%}",
                "predicted_class": predicted_class,
                "enhancement_applied": True,
                "segmentation_completed": True
            }
        }

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({"error": "Analysis failed", "details": str(e)}), 500

    finally:
        # Clean up uploaded file
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    # Pre-load the model
    get_model()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)