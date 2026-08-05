# DeepShield: Live Demonstration Guide

This guide outlines the step-by-step procedure for presenting and demonstrating the QA, DevOps, and Cybersecurity baseline for the AI-powered Digital Media Verification System.

---

## ⚠️ Important Integration Note

> [!WARNING]
> Per project constraints, the HTML templates and frontend interface are managed by other team members. The original template files (`index.html` and `result.html`) have route mismatches with the backend (`app.py` expects `/upload` and parameter `image`, whereas `index.html` submits to `/predict` with parameter `file`).
> 
> To demonstrate the complete backend security and pre-processing pipeline, use the **Automated Testing Suite**. Once the frontend team member updates the HTML form action to `/upload` and the file input name to `image`, the web interface will connect with the backend.

---

## 🛠️ Step 1: Pre-Demo Preparation

Ensure the environment is ready before the evaluators start:

1. **Activate Environment & Start App**:
   ```bash
   .venv\Scripts\activate
   python app.py
   ```
2. **Generate Demo Assets**:
   Run the generator to ensure the test images are available in `tests/test_images/`:
   ```bash
   python tests/generate_test_assets.py
   ```
3. **Open Browser**:
   Navigate to `http://127.0.0.1:5000/` to show the basic interface is running.

---

## 🎭 Step 2: The Demonstration Script

### Part A: Introduction (1 minute)
* **What to say**:
  > "Hello, I am the QA, DevOps & Cybersecurity Lead. For my role, my primary focus was on establishing branching standards, securing the application from upload vulnerabilities, writing automated test suites, and delivering a reliable system ready for integration.
  > While other team members handle the HTML styling and prediction model weights, I have fully implemented and verified the backend security controls."

---

### Part B: Showing Security Controls via Testing (3 minutes)
Demonstrate the application's cybersecurity robustness using the automated suite:

1. **Run the Test Suite**:
   * **Action**: Open the terminal in the project directory and run:
     ```bash
     python -m unittest tests/test_app.py
     ```
   * **Highlight**: Point out that all 7 tests (covering security headers, MIME verification, size limits, and path boundaries) pass successfully (`OK`).

2. **Explain MIME Spoof Checking (Magic Bytes Verification)**:
   * **What to say**:
     > "We have implemented server-side binary signature verification. A common cybersecurity threat is when an attacker renames a malicious script (like a web shell) to `.png` to bypass basic extension checks.
     > Our backend opens the file stream and validates the actual file magic bytes (`b'\x89PNG\r\n\x1a\n'` / `b'\xff\xd8\xff'`). Our automated test `test_upload_disguised_file_fails_signature` confirms that text files disguised as PNGs are successfully flagged and blocked, flashing a `'Security check failed'` error."

3. **Explain Path Traversal Defenses**:
   * **What to say**:
     > "To prevent directory traversal attacks (such as trying to write files to system folders using `../../` path sequences), we use `secure_filename()` to sanitize input names and perform boundary verification to guarantee saved paths resolve strictly within the static upload folder."

4. **Explain Storage Exhaustion & DevOps Protections**:
   * **What to say**:
     > "To prevent Denial of Service via server storage exhaustion, we configure a strict 5MB limit. Furthermore, the system runs an automated cleanup routine that scans and deletes temporary uploads older than 5 minutes while preserving developer assets like `.gitkeep`."

---

### Part C: Code Hardening Overview (2 minutes)
Show the following files to the evaluators:
* **[.env.example](file:///c:/Users/sayan/OneDrive/Desktop/AI-powered-Digital-Media-Verification-System/BCT%20PROJECT/AI-powered-Digital-Media-Verification-System-main/.env.example)**: Show that we manage secrets securely rather than hardcoding keys.
* **[requirements.txt](file:///c:/Users/sayan/OneDrive/Desktop/AI-powered-Digital-Media-Verification-System/BCT%20PROJECT/AI-powered-Digital-Media-Verification-System-main/requirements.txt)**: Show the pinned library versions for reproducible builds.
* **[GIT_STANDARDS.md](file:///c:/Users/sayan/OneDrive/Desktop/AI-powered-Digital-Media-Verification-System/BCT%20PROJECT/AI-powered-Digital-Media-Verification-System-main/GIT_STANDARDS.md)**: Show the branching standard and PR guidelines that governed team development.
