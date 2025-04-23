from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
import numpy as np # type: ignore
import cv2 # type: ignore
from werkzeug.utils import secure_filename

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.image_utils import load_medical_image, enhance_image, segment_image
from model.cnn_model import create_model, preprocess_image

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the model
model = None
UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_model():
    global model
    if model is None:
        model = create_model()
        # TODO: Load trained weights when available
        # model.load_weights('path_to_weights.h5')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "AI Medical Image Analysis System is running"})

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load and process the image
        image = load_medical_image(filepath)
        if image is None:
            return jsonify({"error": "Failed to load image"}), 400

        # Enhance image quality
        enhanced_image = enhance_image(image)
        
        # Perform segmentation
        segmented_image = segment_image(enhanced_image)
        
        # Prepare image for model
        processed_image = preprocess_image(enhanced_image)
        
        # Initialize model if needed
        init_model()
        
        # For now, return processing results
        # TODO: Add actual model prediction when trained
        return jsonify({
            "status": "success",
            "message": "Image processed successfully",
            "details": {
                "original_size": image.shape,
                "enhanced": "Image quality enhanced",
                "segmentation": "Regions identified",
                "analysis": "Preliminary analysis complete"
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)