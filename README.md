# DeepShield: AI-Powered Digital Media Verification System

DeepShield is a Flask-based web application designed to detect synthetic and manipulated media (such as AI-generated deepfakes) and verify the authenticity of digital photographs. 

This repository houses the DevOps, Quality Assurance (QA), and Cybersecurity baseline implementations.

---

## 🛡️ Cybersecurity Hardening Baseline

We have implemented the following core security controls to protect the application from standard web exploitation vectors:

* **Binary Magic Byte Verification**: Standard browsers identify file types by extension. DeepShield parses the first 8 bytes of files at the server side to confirm `b'\x89PNG\r\n\x1a\n'` (for PNG) or `b'\xff\xd8\xff'` (for JPEG) signatures. Executable scripts disguised as image extensions are rejected.
* **Path Traversal Prevention**: Resolves path boundaries using absolute path checking to ensure uploads are locked inside the target folder and filters filenames through `secure_filename()`.
* **HTTP Security Headers**: Injects protection headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection`, `Content-Security-Policy`) to mitigate client-side vulnerabilities.
* **Configuration Hardening**: Employs environment variables (`.env`) for secrets management (e.g., Flask session key) instead of hardcoding keys.

---

## ⚙️ DevOps Best Practices

* **Automated Cleanup**: Programmatically purges uploaded media files older than 5 minutes to mitigate storage leakage (while protecting team workspace configuration files like `.gitkeep`).
* **Pinned Dependencies**: Pin all dependencies (`Flask`, `Pillow`, `numpy`, `python-dotenv`, `Werkzeug`) inside `requirements.txt`.
* **Git Branching Standards**: Standardized workflow documented in `GIT_STANDARDS.md`.

---

## 📂 Project Directory Structure

```text
├── .env                       # Local environment configuration
├── .env.example               # Template environment configuration
├── .gitignore                 # Configured to ignore ML weights, uploads, and venvs
├── GIT_STANDARDS.md           # Git Branching model & PR workflow guidelines
├── README.md                  # Main project documentation (This file)
├── DEMO_GUIDE.md              # Live Demonstration Script & presentation manual
├── app.py                     # Main Flask Server & Route Controllers (Hardened)
├── requirements.txt           # Pinned dependencies
├── model/
│   ├── model.pth              # Machine learning model weights placeholder (Git-ignored)
│   └── predict.py             # Inference pipeline adapter (Managed by Member 3)
├── static/
│   └── uploads/               # Temporary uploads folder
│       └── .gitkeep           # Tracks the empty directory in Git
├── templates/
│   ├── index.html             # Homepage upload template (Managed by other members)
│   └── result.html            # Verification report template (Managed by other members)
├── tests/
│   ├── generate_test_assets.py # Programmatic mock JPG/PNG and spoofed file generator
│   ├── test_app.py            # Hardened Flask app unit tests suite
│   └── test_images/           # Auto-generated test images directory
└── utils/
    └── preprocess.py          # Preprocessing & Security validation functions
```

---

## 🚀 Setup & Installation

### Prerequisites
* Python 3.10 or higher
* `pip` package manager

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd AI-powered-Digital-Media-Verification-System
```

### 2. Set up virtual environment
```bash
# Create environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Copy configuration template
```bash
copy .env.example .env
```

### 5. Launch the Server
```bash
python app.py
```

---

## 🧪 Testing Suite & Verification

The testing suite contains 7 unit tests verifying route access, security headers, file size limits, extension validation, and magic byte verification.

### Running Tests
To programmatically generate test assets and run the suite:

```bash
# Step 1: Generate testing media assets
python tests/generate_test_assets.py

# Step 2: Execute the unit test runner
python -m unittest tests/test_app.py
```
All tests should run and output `OK`.
