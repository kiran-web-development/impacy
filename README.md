# AI Medical Image Analysis System

This system provides AI-powered analysis of medical images using deep learning and computer vision techniques.

## Project Structure
- `frontend/`: Web interface for uploading and viewing medical images
- `backend/`: Flask API server
- `api/`: Image processing utilities
- `model/`: CNN model architecture and training
- `data/`: Storage for uploads and datasets
- `tests/`: Unit tests

## Prerequisites
- Python 3.8+
- pip (Python package manager)
- Web browser with JavaScript enabled

## Setup Instructions

1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create necessary directories:
```bash
mkdir -p data/uploads model/weights
```

5. Set up environment variables by copying `.env.example` to `.env` and adjusting values as needed.

## Running the Application

1. Start the Flask backend server:
```bash
python backend/app.py
```

2. Open the frontend:
Open `frontend/index.html` in a web browser

## Running Tests
```bash
python -m pytest tests/
```

## Features
- Upload medical images (DICOM, JPEG, PNG formats)
- Image enhancement and preprocessing
- AI-powered disease detection
- Real-time analysis results
- HIPAA/GDPR compliant security measures

## Security Notes
- Ensure proper access controls are in place
- Keep environment variables secure
- Regularly update dependencies
- Follow HIPAA compliance guidelines for medical data

## Development
1. Frontend modifications: Edit files in the `frontend/` directory
2. Backend API changes: Modify `backend/app.py`
3. Image processing: Update `api/image_utils.py`
4. Model changes: Modify `model/cnn_model.py`

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.