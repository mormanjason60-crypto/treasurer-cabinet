from datetime import datetime
import json
import os
from flask import Flask, flash, redirect, render_template_string, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "treasurer_cabinet_secure_local_key"

# Define base archival directory structure
BASE_CABINET_DIR = os.path.expanduser("~/Treasurer_Digital_Cabinet")
CATEGORIES = ["Invoices", "Receipts", "Bank_Statements", "Tax_Records"]

# Ensure directories exist
for cat in CATEGORIES:
    os.makedirs(os.path.join(BASE_CABINET_DIR, cat), exist_ok=True)

# Minimal, User-Friendly HTML UI for non-technical users
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Waverly Treasurer - Digital File Cabinet</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; margin-top: 0; }
        label { font-weight: bold; display: block; margin-top: 15px; }
        select, input[type="file"], input[type="submit"] { width: 100%; padding: 10px; margin-top: 8px; border-radius: 4px; border: 1px solid #ccc; box-sizing: border-box; }
        input[type="submit"] { background-color: #27ae60; color: white; font-weight: bold; border: none; cursor: pointer; margin-top: 20px; font-size: 16px; }
        input[type="submit"]:hover { background-color: #219150; }
        .flash { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 4px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📁 Treasurer Document Archival Portal</h2>
        <p>Upload receipts, invoices, or reports to save them automatically into structured cabinet archives.</p>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for msg in messages %}
              <div class="flash">{{ msg }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="category">Document Category:</label>
            <select name="category" id="category" required>
                {% for cat in categories %}
                    <option value="{{ cat }}">{{ cat.replace('_', ' ') }}</option>
                {% endfor %}
            </select>

            <label for="file">Select File (PDF, Image, Doc):</label>
            <input type="file" name="file" id="file" required>

            <input type="submit" value="Upload & Archive File">
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, categories=CATEGORIES)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part in request.")
        return redirect(url_for("index"))

    file = request.files["file"]
    category = request.form.get("category")

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if file and category in CATEGORIES:
        original_name = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_filename = f"{timestamp}_{original_name}"

        # Target directory path
        target_dir = os.path.join(BASE_CABINET_DIR, category)
        file_path = os.path.join(target_dir, archived_filename)

        # Save document
        file.save(file_path)

        # Generate Audit Log Entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "original_filename": original_name,
            "archived_filename": archived_filename,
            "category": category,
            "storage_path": file_path,
            "file_size_bytes": os.path.getsize(file_path),
        }

        # Save metadata entry to central audit index
        log_file = os.path.join(BASE_CABINET_DIR, "audit_index.json")
        logs = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []

        logs.append(log_entry)
        with open(log_file, "w") as f:
            json.dump(logs, f, indent=4)

        flash(
            f"Successfully archived '{original_name}' to {category} folder!"
        )
        return redirect(url_for("index"))

    flash("Invalid upload request.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
