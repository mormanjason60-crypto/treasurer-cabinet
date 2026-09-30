#  Financial Document Archival System

## Overview
A web-based document archival and metadata indexing system built with Python and Flask. Designed for finance workflows, it provides a simple interface for non-technical users to upload financial records while automating file normalization, category directory organization, and structured audit logging.

## Features
* **User-Friendly Portal:** Minimal web interface built for quick file upload across accounting categories (Invoices, Receipts, Bank Statements, Tax Records).
* **Automated Archival Pipeline:** Normalizes filenames with ISO-style timestamps (`YYYYMMDD_HHMMSS_<filename>`) to enforce chronological sorting and avoid file collisions.
* **Metadata Indexing:** Writes structured JSON telemetry records (`audit_index.json`) tracking file pathing, document size, and upload timestamps for compliance reporting.

## Tech Stack
* **Language:** Python 3
* **Framework:** Flask, Werkzeug
* **Environment:** Linux (Debian)
