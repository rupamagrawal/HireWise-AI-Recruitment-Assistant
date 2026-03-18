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

## Project Structure


.
├── data/
│ ├── resumes/
│ └── job_descriptions.csv
│
├── parsed_data/
│ ├── parsed_resumes.json
│ └── parsed_jobs.json
│
├── output/
│ ├── match_results.csv
│ └── shortlisted_candidates.csv
│
├── scripts/
│ ├── extract_pdfs.py
│ ├── load_jobs.py
│ └── run_matching.py
│
├── utils/
│ └── ollama_utils.py
│
├── main.py
├── send_emails.py
├── requirements.txt


---

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
