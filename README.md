# HireWise AI – Recruitment Assistant

An end-to-end AI-powered recruitment pipeline that automates resume screening, candidate scoring, shortlisting, and interview scheduling.

## Overview

HireWise AI reads PDF resumes and job descriptions, uses an LLM to evaluate how well each candidate fits each role, ranks them by match score, and automatically emails interview invitations to shortlisted candidates. **Groq** (cloud) is the primary LLM provider for fast, low-latency scoring; **Ollama** (local) is kept as an offline fallback.

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
│   └── run_matching.py             # Orchestrates LLM-based scoring
│
├── utils/
│   ├── llm_router.py               # Routes calls: Groq (primary) → Ollama (fallback)
│   └── ollama_utils.py             # Ollama API wrapper (offline fallback)
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
- **Groq** – Primary cloud LLM provider for candidate scoring (fast, low-latency)
- **Ollama** – Offline/local LLM fallback for candidate scoring
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

**3. Create a `.env` file** (copy `.env.example` and fill in your values)

```env
# Groq – primary LLM (get a free key at https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Ollama – offline fallback (only needed if Groq is unavailable)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi

# Email
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
3. For each resume-job pair, `utils/llm_router.py` selects the LLM backend:
   - **Groq** is used when `GROQ_API_KEY` is present in `.env` (fast cloud inference)
   - **Ollama** is used as a fallback when `GROQ_API_KEY` is not set, or if the Groq
     API call fails or times out (failure is logged; Ollama is tried transparently)
4. The LLM returns a match score (0–100)
5. Candidates scoring ≥ 80 are written to `shortlisted_candidates.csv`
6. Interview invitation emails are sent automatically via Gmail SMTP

## Output

| File                       | Description                                |
|----------------------------|--------------------------------------------|
| `output/match_results.csv` | All candidates with their job match scores |
| `output/shortlisted_candidates.csv` | Candidates with score ≥ 80        |

## Notes

- **Groq** is the default LLM provider. Set `GROQ_API_KEY` in `.env` to enable it.
- **Ollama** is the offline fallback. The pipeline falls back to Ollama automatically if
  `GROQ_API_KEY` is not set or the Groq API call fails/times out — no manual switching needed.
- To run Ollama locally: `ollama run phi` (or whichever model is set in `OLLAMA_MODEL`)
- Candidate email is extracted from resume text using regex
- The shortlist threshold (80) can be adjusted in `run_matching.py`
- Gmail requires an [App Password](https://support.google.com/accounts/answer/185833) for SMTP

## Author

**Rupam Agrawal**  
[GitHub](https://github.com/rupamagrawal) · [LinkedIn](https://www.linkedin.com/in/rupam-agrawal-09777b278/)
