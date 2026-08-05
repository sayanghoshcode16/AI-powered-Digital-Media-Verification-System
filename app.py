import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from utils.preprocess import is_allowed_file, validate_and_preprocess_image, cleanup_old_uploads

app = Flask(__name__)
app.secret_key = "deepshield_secret_key_change_in_production"

# Configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB Max limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- TEMPORARY MOCK INFERENCE (Replaced when Member 3 delivers predict.py) ---
def mock_predict_image(image_tensor):
    """Dummy AI engine used for testing before Member 3 finishes."""
    import random
    confidence = round(random.uniform(0.65, 0.98), 3)
    is_fake = random.choice([True, False])
    
    prediction = "AI-generated" if is_fake else "Real Photograph"
    
    # Assign risk level based on confidence
    if not is_fake:
        risk_level = "Low"
    elif confidence > 0.85:
        risk_level = "High"
    else:
        risk_level = "Moderate"
        
    return {
        "prediction": prediction,
        "confidence": f"{round(confidence * 100, 1)}%",
        "risk_level": risk_level
    }


@app.route('/')
def index():
    # Clean up old uploaded files whenever the main page opens
    cleanup_old_uploads(app.config['UPLOAD_FOLDER'])
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    # 1. Check if file part is in request
    if 'image' not in request.files:
        flash("No image file provided in request.", "error")
        return redirect(url_for('index'))
    
    file = request.files['image']
    
    if file.filename == '':
        flash("No file selected.", "error")
        return redirect(url_for('index'))
        
    # 2. Check extension & secure file name with UUID (Prevents Path Traversal)
    if file and is_allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(saved_path)
        
        # 3. Validate & Preprocess image (Member 4 pipeline)
        processed_tensor, _ = validate_and_preprocess_image(saved_path)
        
        if processed_tensor is None:
            # Delete corrupted/invalid file
            if os.path.exists(saved_path):
                os.remove(saved_path)
            flash("Invalid or corrupted image file.", "error")
            return redirect(url_for('index'))
            
        # 4. Pass tensor to prediction model
        # (Using mock until Member 3 integrates predict.py)
        result = mock_predict_image(processed_tensor)
        
        # Image URL for display on result page
        image_url = url_for('static', filename=f'uploads/{unique_filename}')
        
        return render_template(
            'result.html',
            image_url=image_url,
            prediction=result['prediction'],
            confidence=result['confidence'],
            risk_level=result['risk_level']
        )
        
    flash("File type not allowed. Please upload JPG, JPEG, or PNG.", "error")
    return redirect(url_for('index'))


@app.errorhandler(413)
def file_too_large(error):
    """Handle 5MB file size excess gracefully."""
    flash("File size exceeds 5MB limit. Please upload a smaller file.", "error")
    return redirect(url_for('index')), 413


if __name__ == '__main__':
    app.run(debug=True, port=5000)