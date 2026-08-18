Pharma Complaint Management System

An AI-powered pharmaceutical complaint management system that converts unstructured customer complaints into structured data and performs initial severity/priority assessment.

🚀 Features

AI-based complaint information extraction

LangGraph multi-step AI workflow

Severity classification: Critical / Major / Minor

Priority classification: High / Medium / Low

PDF, DOCX and TXT text extraction

FastAPI REST APIs

React frontend with AI-assisted form auto-fill

PostgreSQL database with SQLAlchemy

Environment-based API key configuration

🏗️ Architecture

flowchart LR
    A[User] --> B[React Frontend]
    B --> C[FastAPI]
    C --> D[LangGraph]

    D --> E[Extract Complaint Info]
    E --> F[Risk & Severity Classification]

    F --> G[Structured JSON]
    G --> B

    B -->|Save Complaint| C
    C --> H[(PostgreSQL)]

🤖 AI Workflow

flowchart TD
    A[Complaint Text / Document] --> B[Text Extraction]
    B --> C[LangGraph State]
    C --> D[LLM: Information Extraction]
    D --> E[Structured Complaint Data]
    E --> F[LLM: Risk Assessment]
    F --> G[Severity + Priority + Reasoning]
    G --> H[Final JSON Response]

Extracted Information

The AI extracts:

Customer name

Product name & strength

Batch number

Manufacturing / expiry date

Quantity affected

Complaint source & type

Complaint date

Complaint description

Risk Assessment

The AI classifies complaints into:

Severity

Example

Critical

Patient safety risk, contamination, wrong dosage

Major

Packaging damage, labeling error

Minor

Cosmetic/minor issue

🛠️ Tech Stack

Backend

Python

FastAPI

LangGraph

Groq

Pydantic

SQLAlchemy

PostgreSQL

Frontend

React

Redux

JavaScript / JSX

CSS

Document Processing

pypdf

python-docx

📁 Project Structure

project/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── complaint_agent.py
│   │   ├── api/
│   │   │   └── complaints.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   └── complaint.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── redux/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
└── README.md

⚙️ Setup

1. Clone Repository

git clone <your-repository-url>
cd project

2. Backend

cd backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

3. Environment Variables

Create .env inside backend/:

GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/complaints_db

EXTRACTION_MODEL=openai/gpt-oss-20b
REASONING_MODEL=openai/gpt-oss-120b

Never commit .env or API keys to GitHub.

4. PostgreSQL

Create the database:

CREATE DATABASE complaints_db;

The application creates the required table automatically when the backend starts.

5. Start Backend

uvicorn app.main:app --reload

API:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

6. Start Frontend

cd frontend
npm install
npm run dev

🔌 API Endpoints

Method

Endpoint

Purpose

GET

/

Health check

POST

/api/complaints/extract-from-text

Extract complaint from text

POST

/api/complaints/extract-from-file

Extract complaint from PDF/DOCX/TXT

POST

/api/complaints/

Save complaint

GET

/api/complaints/

List complaints

GET

/api/complaints/{id}

Get single complaint

📦 Example Response

{
  "complaint_source": "Email",
  "customer_name": "Abhayraj",
  "product_name": "Paracetamol",
  "product_strength": "500 mg",
  "batch_number": "B12345",
  "complaint_type": "Packaging Issue",
  "complaint_description": "Customer reported damaged packaging.",
  "initial_severity": "Major",
  "priority": "Medium",
  "ai_confidence_notes": "The complaint indicates a quality issue without immediate safety risk."
}

🔐 Production Improvements

For a production deployment, consider adding:

Authentication & role-based access

OCR for scanned PDFs

Alembic database migrations

File size/content validation

Audit logging

Rate limiting

Better AI confidence/uncertainty handling

Human approval workflow

AI output is intended for initial triage and should be reviewed by a qualified human before regulated quality or patient-safety decisions.

👨‍💻 Author

Abhay Raj

Computer Science & Engineering

Built with Python • FastAPI • React • LangGraph • Groq • PostgreSQL
