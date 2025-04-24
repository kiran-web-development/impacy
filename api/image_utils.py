import cv2
import numpy as np
import pydicom
from PIL import Image
import io

def load_medical_image(file_path_or_bytes):
    """
    Load medical image from various formats (DICOM, JPEG, PNG)
    Supports both file paths and bytes/BytesIO input
    """
    try:
        if isinstance(file_path_or_bytes, (str, bytes, io.BytesIO)):
            if isinstance(file_path_or_bytes, str):
                if file_path_or_bytes.lower().endswith('.dcm'):
                    return load_dicom(file_path_or_bytes)
                # Fast load using PIL for common formats
                img = Image.open(file_path_or_bytes)
                return np.array(img)
            else:
                # Handle bytes/BytesIO input
                img = Image.open(io.BytesIO(file_path_or_bytes) if isinstance(file_path_or_bytes, bytes) else file_path_or_bytes)
                return np.array(img)
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return None

def load_dicom(file_path):
    """
    Load and process DICOM image with optimized processing
    """
    try:
        dicom = pydicom.dcmread(file_path)
        image = dicom.pixel_array.astype(float)
        
        # Faster normalization using vectorized operations
        min_val = image.min()
        max_val = image.max()
        if max_val != min_val:
            image = ((image - min_val) * (255.0 / (max_val - min_val))).astype(np.uint8)
        else:
            image = np.zeros_like(image, dtype=np.uint8)
        
        return image
    except Exception as e:
        print(f"Error loading DICOM: {str(e)}")
        return None

def enhance_image(image):
    """
    Enhance medical image quality with optimized processing
    """
    try:
        # Create CLAHE object only once
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        
        if len(image.shape) == 2:
            return clahe.apply(image)
        
        # Optimize color image processing
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel = clahe.apply(lab[:,:,0])
        lab[:,:,0] = l_channel
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    except Exception as e:
        print(f"Error enhancing image: {str(e)}")
        return image

def segment_image(image):
    """
    Perform optimized image segmentation
    """
    try:
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use faster Otsu's thresholding
        thresh_value, binary = cv2.threshold(
            blurred, 0, 255, 
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        
        return binary
    except Exception as e:
        print(f"Error segmenting image: {str(e)}")
        return None