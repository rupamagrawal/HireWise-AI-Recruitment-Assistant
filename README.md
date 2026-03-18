# HireWise AI – Recruitment Assistant

An end-to-end AI-powered recruitment pipeline that automates resume screening, candidate scoring, shortlisting, and interview scheduling.

## Overview

HireWise AI reads PDF resumes and job descriptions, uses a local LLM (Ollama) to evaluate how well each candidate fits each role, ranks them by match score, and automatically emails interview invitations to shortlisted candidates.

## Project Structure

```
HireWise-AI-Recruitment-Assistant/
│
├── data/
│   ├── resumes/                    # Input resume PDFs
│   └── job_descriptions.csv        # Input job descriptions
│
├── parsed_data/
│   ├── parsed_resumes.json         # Extracted resume text
│   └── parsed_jobs.json            # Structured job data
│
├── output/
│   ├── match_results.csv           # All candidate-job scores
│   └── shortlisted_candidates.csv  # Shortlisted candidates
│
├── scripts/
│   ├── extract_pdfs.py             # PDF text extraction
│   ├── load_jobs.py                # Job description processing
│   └── run_matching.py             # LLM-based scoring logic
│
├── utils/
│   └── ollama_utils.py             # Ollama API wrapper
│
├── main.py                         # Runs the full pipeline
├── send_emails.py                  # Sends interview invites
├── requirements.txt
├── .env.example
└── .gitignore
```
```
## Tech Stack

- **Python** – Core language
- **PyMuPDF (fitz)** – PDF parsing
- **Pandas** – CSV/data processing
- **Ollama** – Local LLM inference for candidate scoring
- **SMTP (Gmail)** – Email automation
- **python-dotenv** – Environment variable management

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Install and run Ollama**

```bash
ollama run phi
```

**3. Create a `.env` file**

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## Usage

Run the full pipeline (extract → match → shortlist):

```bash
python main.py
```

Send interview emails to shortlisted candidates:

```bash
python send_emails.py
```

## How It Works

1. Resume PDFs are parsed into raw text using PyMuPDF
2. Job descriptions are loaded from CSV and structured as JSON
3. For each resume-job pair, the LLM returns a match score (0–100)
4. Candidates scoring ≥ 80 are written to `shortlisted_candidates.csv`
5. Interview invitation emails are sent automatically via Gmail SMTP

## Output

| File                       | Description                                |
|----------------------------|--------------------------------------------|
| `output/match_results.csv` | All candidates with their job match scores |
| `output/shortlisted_candidates.csv` | Candidates with score ≥ 80        |

## Notes

- Ollama must be running locally before executing the pipeline
- Candidate email is extracted from resume text using regex
- The shortlist threshold (80) can be adjusted in `run_matching.py`
- Gmail requires an [App Password](https://support.google.com/accounts/answer/185833) for SMTP

## Author

**Rupam Agrawal**  
[GitHub](https://github.com/rupamagrawal) · [LinkedIn](https://www.linkedin.com/in/rupam-agrawal-09777b278/)
