import os
import time
from PIL import Image, ImageOps
import numpy as np

# Standard constants
IMAGE_SIZE = (224, 224)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def is_allowed_file(filename: str) -> bool:
    """Checks if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_and_preprocess_image(file_path: str):
    """
    Validates, opens, converts to RGB, resizes, and normalizes image.
    Returns:
        tuple: (processed_numpy_array, PIL_Image_object) or (None, None) if invalid.
    """
    try:
        # Open and verify image integrity (catches corrupted/fake image files)
        with Image.open(file_path) as img:
            img.verify()  # Verifies file integrity
            
        # Re-open for actual processing (verify closes file pointer)
        img = Image.open(file_path)
        
        # 1. Convert to RGB (handles PNG transparency/RGBA & Grayscale)
        img_rgb = img.convert('RGB')
        
        # 2. Resize to standard dimensions (224 x 224)
        img_resized = img_rgb.resize(IMAGE_SIZE, Image.Resampling.BILINEAR)
        
        # 3. Convert to NumPy array & Normalize pixels to [0, 1]
        img_array = np.array(img_resized, dtype=np.float32) / 255.0
        
        # 4. Standard PyTorch format: Transpose from (H, W, C) -> (C, H, W)
        img_tensor_format = np.transpose(img_array, (2, 0, 1))
        
        return img_tensor_format, img_resized

    except Exception as e:
        print(f"[Preprocessing Error] File {file_path} failed validation: {e}")
        return None, None

def cleanup_old_uploads(folder_path: str, max_age_seconds: int = 300):
    """
    Task 4.3: Deletes temporary uploaded files older than max_age_seconds (default 5 minutes).
    """
    if not os.path.exists(folder_path):
        return

    now = time.time()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                try:
                    os.remove(file_path)
                    print(f"[Cleanup] Deleted temporary file: {filename}")
                except Exception as e:
                    print(f"[Cleanup Error] Could not delete {filename}: {e}")