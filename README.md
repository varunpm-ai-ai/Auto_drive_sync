# Auto Drive Sync

## Intelligent WhatsApp → Google Drive Ingestion & Organization System**

![High Level Design](docs/images/hld.png)
![Low Level Design](docs/images/lld.png)

---

## Overview

**Auto Drive Sync** is an event-driven document ingestion system that continuously monitors **WhatsApp Desktop downloads**, intelligently classifies incoming files, and automatically organizes them into a structured **Google Drive hierarchy**.

The system is designed to handle **real-world messy data** (generic filenames, scanned PDFs, images, certificates) while remaining **safe, explainable, and conservative**.  
Files are auto-routed only when confidence is high; otherwise, they are escalated for **manual review**.

This project focuses on **system design, decision intelligence, and scalability**, not just automation.

---

## Main Goals

- Zero manual sorting of WhatsApp academic documents
- Safe automation (no silent misclassification)
- Explainable decisions with confidence scores
- Future-proof design for ML upgrades (v2)

---

## How the System Works

WhatsApp Desktop
↓
Filesystem Watcher
↓
Metadata Extraction
↓
Rule-Based Classification
↓
Decision Engine
↓
(Content Peek if needed)
↓
Final Decision
↓
Google Drive Upload


---

##  Core Components

### 1️ Watcher (`watcher.py`)

- Monitors WhatsApp Desktop `transfers/` directory recursively
- Detects file creation/modification events
- Emits file paths into the pipeline
- Handles graceful startup and shutdown

---

### 2️ Metadata Extractor (`metadata.py`)

- Extracts:
  - filename, extension
  - timestamps
  - size
- Normalizes file information for downstream logic

---

### 3️ Classifier (`classifier.py`) — **Rule-Based (v1)**

- Classifies files using filename heuristics
- Detects:
  - Subject (Machine Learning, Cloud Computing, DevOps, etc.)
  - Content Type (Notes, Assignments, Manuals, QPs)
  - Module number (for Notes)
- Produces:
  - Confidence score
  - Human-readable reasoning

---

### 4️ Content Peek (`content_peek.py`)

Triggered **only when confidence is low**.

- PDF:
  - Detects digital text vs scanned content
  - Extracts first-page keywords
- Images:
  - Applies basic heuristics (handwritten likelihood)
- Never invents meaning — only provides signals

---

### 5️ Decision Engine (`decision.py`)

Determines **what to do**, not **what the file is**.

Possible outcomes:

- `AUTO_ROUTE`
- `NEEDS_CONTENT_PEEK`
- `MANUAL_REVIEW`

Decisions are:

- deterministic
- explainable
- confidence-driven

---

### 6️ Organizer (`organizer.py`)

Maps classification + decision into a **logical Drive path**.

Example structure:

``` bash 
6th Sem College/
├── Machine Learning/
│ ├── Notes/
│ │ ├── Module 1/
│ │ └── Module 2/
│ ├── Assignments/
│ └── QPs/
├── Labs/
│ ├── DevOps Lab/
│ └── ML Lab/
└── Manual Intervention Review/

```

### 7 Uploader (`uploader.py`)

- Creates folders dynamically in Google Drive
- Uploads files using Drive API
- Handles authentication and permissions
- Logs upload results with file IDs

---

### 8️ Pipeline (`pipeline.py`)

The **brain orchestrator**:

- Runs classification
- Escalates to content peek when needed
- Re-classifies safely
- Produces a final, immutable outcome

No infinite loops. No forced routing.

---

## Logging & Observability

- Centralized logging (`logs/app.log`)
- Logs:
  - filesystem events
  - classification decisions
  - routing paths
  - upload results
- Console logging optional (dev mode)

---

## What Works in v1 (Stable)

- Real-time WhatsApp monitoring
- Safe automatic Google Drive uploads
- Manual review fallback for:
  - generic filenames
  - certificates
  - images
  - scanned PDFs
- Correct lab manual routing even with generic names
- Graceful shutdown and restart
- Production-grade modular architecture

---

## Design Philosophy

> **Conservative automation is better than confident mistakes.**

The system prefers **manual review** over misclassification.  
Every decision is explainable and reversible.

---

## What’s Coming in v2

### Intelligence Upgrades

- NLP-based content understanding
- Keyword → subject inference from document text
- ML classifier (trained on real data)
- Adaptive confidence scoring

### System Enhancements

- File stability detection (partial downloads)
- Duplicate detection (hash-based)
- Event debouncing
- Retry & backoff for uploads
- Optional dashboard for monitoring

---

## Tech Stack

- Python 3.10+
- Watchdog
- Google Drive API
- PyPDF / Pillow
- pathlib, dataclasses, typing
- Structured logging

---

## 📦 Project Status

**Version:** `v1.0 – Stable`  
**Next Milestone:** `v2.0 – ML-Powered Classification`

---

## 👤 Author

Built as a **systems-first engineering project** with emphasis on:

- correctness
- scalability
- real-world constraints
- clean architecture

---

> This project is intentionally designed to evolve.  
> v1 proves the system. v2 will teach it to think.

## How to Use This Project

### Open Source & Forkable

This project is **fully open source**.  
You are free to **fork, modify, and run it locally** for personal use, academic automation, or further experimentation.

---

## Prerequisites

Make sure you have:

- Python **3.10+**
- **WhatsApp Desktop (Windows)**
- A **Google account**
- Basic familiarity with running Python scripts

---

## Quick Start

### 1️ Fork & Clone

```bash
git clone https://github.com/your-username/auto-drive-sync.git
cd auto-drive-sync
```

### 2 Create Venv ( Virtual Environment )

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux / macOS
```

### 3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4 Setup Google drive API

#### 1. Create Google Cloud Project

- Visit https://console.cloud.google.com/
- Create a new project

#### 2. Enable Drive API

- APIs & Services → Enable APIs
- Enable Google Drive API

#### Step 3 — OAuth Consent Screen

- User type: External
- Add yourself as a Test User
- Scope:

```bash
https://www.googleapis.com/auth/drive.file

```

#### 4 Create OAuth Credentials

- Create OAuth Credentials
- Application type: Desktop App
- Application type: Desktop App
- Download credentials.json

#### 5 Authenticate Once

```bash
python scripts/drive_auth_test.py

```

#### 6 Configure WhatsApp Watch Path

```bash 

WATCH_PATH = Path(
    r"C:\Users\YOUR_USERNAME\AppData\Local\Packages"
    r"\5319275A.WhatsAppDesktop_cv1g1gvanyjgm"
    r"\LocalState\sessions"
    r"\YOUR_SESSION_ID"
    r"\transfers"
)

```

- YOUR_SESSION_ID is unique per system.
- Locate it once via File Explorer.

#### Run the system 

```bash

python ./main.py

```

#### Logs

logs are written to 

```bash
logs/app.log

```

## 🤝 Contributing

### Contributions are welcome

- Fork the repository
- Create a feature branch
- Commit clean changes
- Open a pull request