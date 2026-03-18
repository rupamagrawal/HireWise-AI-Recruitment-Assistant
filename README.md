# HireWise AI – Resume Matching System

HireWise AI is a Python-based recruitment assistant that automates resume parsing, job matching, candidate shortlisting, and interview email notifications.

---

## Overview

This project processes resumes and job descriptions, evaluates candidate-job fit using an LLM (via Ollama), and generates ranked results along with shortlisted candidates.

---

## Features

- Extracts text from PDF resumes
- Loads and processes job descriptions from CSV
- Evaluates candidate-job match using LLM-based scoring
- Generates match results with scores (0–100)
- Automatically shortlists top candidates
- Sends interview invitation emails to shortlisted candidates
- End-to-end pipeline execution

---

Yeah your current structure in the screenshot is messy (flattened + hard to read).
Here’s a **clean, proper GitHub-standard project structure** you should use 👇

---

```markdown
## Project Structure

```

HireWise-AI/
│
├── data/
│   ├── resumes/                      # Raw resume PDFs
│   └── job_descriptions.csv         # Input job descriptions
│
├── parsed_data/
│   ├── parsed_resumes.json          # Extracted resume text
│   └── parsed_jobs.json             # Processed job data
│
├── output/
│   ├── match_results.csv            # All candidate-job scores
│   └── shortlisted_candidates.csv   # Candidates with high scores
│
├── scripts/
│   ├── extract_pdfs.py              # Extract text from resumes
│   ├── load_jobs.py                 # Process job descriptions
│   └── run_matching.py              # LLM-based matching logic
│
├── utils/
│   └── ollama_utils.py              # Ollama API interaction
│
├── main.py                          # Runs complete pipeline
├── send_emails.py                   # Sends interview emails
├── requirements.txt                 # Dependencies
├── .env                             # Environment variables (not committed)
├── .gitignore
└── README.md

```
```
## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
2. Setup environment variables

Create a .env file:

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
3. Run Ollama
ollama run phi
Usage

Run the full pipeline:

python main.py

Send emails to shortlisted candidates:

python send_emails.py
Workflow

Extract resume text from PDFs

Load and structure job descriptions

Evaluate resume-job match using LLM

Assign score (0–100)

Store results in CSV

Shortlist candidates with high scores

Send interview emails

Output
match_results.csv
Job Title	Candidate Name	Email	Match Score
shortlisted_candidates.csv

Contains candidates with score ≥ 80

Tech Stack

Python

PyMuPDF

Pandas

Ollama (LLM)

Regex

SMTP (Email)

dotenv

Notes

LLM is used to generate match scores based on job and resume relevance

Email is extracted from resume text using regex

Default shortlist threshold is 80

Ollama must be running locally before executing matching
