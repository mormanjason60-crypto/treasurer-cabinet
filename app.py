import json
import os
from datetime import datetime
from flask import (
    Flask,
    flash,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "bink_vault_secure_key"

BASE_CABINET_DIR = os.path.expanduser("~/Treasurer_Digital_Cabinet")
CATEGORIES = ["Invoices", "Receipts", "Bank_Statements", "Tax_Records"]

for cat in CATEGORIES:
    os.makedirs(os.path.join(BASE_CABINET_DIR, cat), exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BINK - Document Vault & Financial Archival</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            /* NC Blue & White Palette */
            --nc-blue: #7BAFD4;
            --nc-blue-dark: #4B82AA;
            --nc-blue-light: #F0F6FA;
            --bg-color: #F8FAFC;
            --surface-color: #FFFFFF;
            --surface-border: #E2E8F0;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --accent-success: #10B981;
            --card-shadow: 0 10px 25px -5px rgba(123, 175, 212, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
        }

        * { box-sizing: border-box; transition: all 0.2s ease-in-out; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }

        .container { max-width: 1100px; margin: 0 auto; }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 24px;
            border-bottom: 2px solid var(--nc-blue);
            margin-bottom: 32px;
        }

        .brand { display: flex; align-items: center; gap: 16px; }
        .brand-icon {
            background-color: var(--nc-blue);
            color: #FFFFFF;
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            box-shadow: 0 4px 14px rgba(123, 175, 212, 0.4);
        }
        
        .brand h1 { 
            margin: 0; 
            font-size: 24px; 
            font-weight: 700; 
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }
        .brand p { margin: 2px 0 0 0; font-size: 13px; color: var(--nc-blue-dark); font-weight: 500; }

        .grid-layout {
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 28px;
        }

        @media (max-width: 850px) {
            .grid-layout { grid-template-columns: 1fr; }
        }

        .card {
            background-color: var(--surface-color);
            border: 1px solid var(--surface-border);
            border-top: 4px solid var(--nc-blue);
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--card-shadow);
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--surface-border);
        }

        .card-title {
            margin: 0;
            font-size: 16px;
            font-weight: 700;
            color: var(--nc-blue-dark);
        }

        label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-secondary);
            display: block;
            margin-top: 18px;
            margin-bottom: 6px;
        }

        input[type="text"], select, input[type="file"] {
            width: 100%;
            background-color: var(--nc-blue-light);
            border: 1px solid var(--surface-border);
            border-radius: 8px;
            padding: 11px 14px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
        }

        input[type="text"]:focus, select:focus {
            border-color: var(--nc-blue);
            box-shadow: 0 0 0 3px rgba(123, 175, 212, 0.25);
        }

        input[type="file"]::file-selector-button {
            background-color: var(--nc-blue);
            color: #FFFFFF;
            font-weight: 700;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            margin-right: 12px;
        }

        input[type="file"]::file-selector-button:hover {
            background-color: var(--nc-blue-dark);
        }

        .btn-primary {
            width: 100%;
            background-color: var(--nc-blue);
            color: #FFFFFF;
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: none;
            padding: 13px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 24px;
            box-shadow: 0 4px 14px rgba(123, 175, 212, 0.4);
        }

        .btn-primary:hover {
            background-color: var(--nc-blue-dark);
            transform: translateY(-1px);
        }

        .search-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .search-container input { flex-grow: 1; }

        .btn-search {
            background-color: var(--nc-blue-light);
            color: var(--nc-blue-dark);
            border: 1px solid var(--nc-blue);
            border-radius: 8px;
            padding: 0 20px;
            font-weight: 600;
            cursor: pointer;
        }

        .btn-search:hover {
            background-color: var(--nc-blue);
            color: #FFFFFF;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th {
            text-align: left;
            padding: 12px 14px;
            color: var(--nc-blue-dark);
            font-weight: 700;
            border-bottom: 2px solid var(--nc-blue-light);
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.08em;
        }

        td {
            padding: 14px;
            border-bottom: 1px solid var(--surface-border);
            color: var(--text-primary);
        }

        tr:hover td { background-color: var(--nc-blue-light); }

        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            background-color: var(--nc-blue-light);
            color: var(--nc-blue-dark);
            border: 1px solid var(--nc-blue);
        }

        .btn-access {
            display: inline-block;
            padding: 6px 14px;
            background-color: #ECFDF5;
            color: var(--accent-success);
            border: 1px solid #A7F3D0;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 12px;
        }

        .btn-access:hover {
            background-color: var(--accent-success);
            color: #FFFFFF;
        }

        .flash {
            background-color: #ECFDF5;
            border: 1px solid #A7F3D0;
            color: var(--accent-success);
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 24px;
            font-size: 14px;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="navbar">
            <div class="brand">
                <div class="brand-icon">🦋</div>
                <div>
                    <h1>BINK</h1>
                    <p>Municipal Financial Archival & Vault System</p>
                </div>
            </div>
        </div>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for msg in messages %}
              <div class="flash">✓ {{ msg }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="grid-layout">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Archive Document</h3>
                </div>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <label for="company">Entity / Vendor Name</label>
                    <input type="text" name="company" id="company" placeholder="e.g. Amazon, Dominion Energy" required>

                    <label for="category">Record Category</label>
                    <select name="category" id="category" required>
                        {% for cat in categories %}
                            <option value="{{ cat }}">{{ cat.replace('_', ' ') }}</option>
                        {% endfor %}
                    </select>

                    <label for="file">Source File</label>
                    <input type="file" name="file" id="file" required>

                    <button type="submit" class="btn-primary">Upload to BINK Vault</button>
                </form>
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Document Vault & Audit Logs</h3>
                    <span style="font-size: 12px; color: var(--nc-blue-dark); font-weight: 600;">Indexed: {{ logs|length }} Records</span>
                </div>

                <form method="get" action="/" class="search-container">
                    <input type="text" name="q" placeholder="Search by vendor, date (YYYY-MM-DD), or category..." value="{{ query }}">
                    <button type="submit" class="btn-search">Search</button>
                    {% if query %}
                        <a href="/" style="align-self: center; font-size: 13px; text-decoration: none; color: var(--text-secondary);">Clear</a>
                    {% endif %}
                </form>

                {% if logs %}
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Entity / Vendor</th>
                            <th>Category</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for log in logs|reverse %}
                        <tr>
                            <td>{{ log.timestamp[:10] }}</td>
                            <td><strong>{{ log.company }}</strong></td>
                            <td><span class="badge">{{ log.category.replace('_', ' ') }}</span></td>
                            <td>
                                <a class="btn-access" href="/download/{{ log.category }}/{{ log.archived_filename }}" target="_blank">Access File</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p style="color: var(--text-secondary); text-align: center; padding: 40px 0;">No matching records found in BINK vault.</p>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()
    log_file = os.path.join(BASE_CABINET_DIR, "audit_index.json")
    logs = []

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    if query:
        filtered_logs = []
        for log in logs:
            company = log.get("company", "").lower()
            cat = log.get("category", "").lower()
            fname = log.get("original_filename", "").lower()
            date = log.get("timestamp", "")[:10]

            if (
                query in company
                or query in cat
                or query in fname
                or query in date
            ):
                filtered_logs.append(log)
        logs = filtered_logs

    return render_template_string(
        HTML_TEMPLATE, categories=CATEGORIES, logs=logs, query=query
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file included in request.")
        return redirect(url_for("index"))

    file = request.files["file"]
    category = request.form.get("category")
    company = request.form.get("company", "Unspecified").strip()

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if file and category in CATEGORIES:
        original_name = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_company = (
            "".join(
                c for c in company if c.isalnum() or c in (" ", "_", "-")
            )
            .strip()
            .replace(" ", "_")
        )
        archived_filename = f"{timestamp}_{sanitized_company}_{original_name}"

        target_dir = os.path.join(BASE_CABINET_DIR, category)
        file_path = os.path.join(target_dir, archived_filename)

        file.save(file_path)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "company": company,
            "original_filename": original_name,
            "archived_filename": archived_filename,
            "category": category,
            "storage_path": file_path,
            "file_size_bytes": os.path.getsize(file_path),
        }

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
            f"Successfully archived document for '{company}' into BINK {category.replace('_', ' ')}!"
        )
        return redirect(url_for("index"))

    flash("Invalid request parameters.")
    return redirect(url_for("index"))


@app.route("/download/<category>/<filename>")
def download_file(category, filename):
    if category not in CATEGORIES:
        return "Invalid category", 400
    directory = os.path.join(BASE_CABINET_DIR, category)
    return send_from_directory(directory, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
