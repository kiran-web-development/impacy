import cv2
import numpy as np
import pydicom

def load_medical_image(file_path):
    """
    Load medical image from various formats (DICOM, JPEG, PNG)
    """
    if file_path.lower().endswith('.dcm'):
        return load_dicom(file_path)
    return cv2.imread(file_path)

def load_dicom(file_path):
    """
    Load and process DICOM image
    """
    dicom = pydicom.dcmread(file_path)
    image = dicom.pixel_array.astype(float)
    # Normalize to 0-255 range
    image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
    return image

def enhance_image(image):
    """
    Enhance medical image quality
    """
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    if len(image.shape) == 2:  # Grayscale image
        return clahe.apply(image)
    
    # For RGB images, apply CLAHE to luminance channel
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def segment_image(image):
    """
    Perform basic image segmentation
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Apply Otsu's thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary