import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import csv
import re
from dotenv import load_dotenv
from utils.ollama_utils import query_ollama

load_dotenv()

# Load resumes and jobs
with open("parsed_data/parsed_resumes.json", "r", encoding="utf-8") as f:
    resumes = json.load(f)

with open("parsed_data/parsed_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)


def extract_score(text):
    try:
        match = re.search(r"\b(\d{1,3})\b", text)
        if match:
            score = int(match.group(1))
            if 0 <= score <= 100:
                return score
    except:
        pass
    return 0


def get_score_from_model(job_description, resume_text):
    prompt = f"""
You are a strict AI evaluator.

Given a job and a resume, respond with a SINGLE number from 0 to 100 that represents the match score.

DO NOT respond with explanation, just the number.

Job: {job_description[:200]}

Resume: {resume_text[:200]}

Score:
"""
    ollama_response = query_ollama(prompt)
    print(f"\n🧠 Ollama response:\n{ollama_response}\n")

    if ollama_response:
        if "sorry" in ollama_response.lower() or "not able" in ollama_response.lower():
            print("⚠️ Skipping irrelevant response.")
            return 0

        score = extract_score(ollama_response)
        print(f"🎯 Parsed Score: {score}")
        return score

    print("❌ No valid score parsed. Returning 0.")
    return 0


def evaluate_applicant_for_job(resume_filename, resume_text, job_title, job_description):
    resume_text = resume_text[:2000]
    score = get_score_from_model(job_description, resume_text)
    print(f"✅ Final Score for {resume_filename} → {job_title}: {score}")

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", resume_text)
    candidate_email = email_match.group(0) if email_match else "unknown@example.com"

    return {
        "job_title": job_title,
        "name": resume_filename,
        "email": candidate_email,
        "score": score,
        "explanation": "Score based on job-resume relevance."
    }


# Output CSVs
os.makedirs("output", exist_ok=True)
with open("output/match_results.csv", "w", newline="", encoding="utf-8") as f_results, \
     open("output/shortlisted_candidates.csv", "w", newline="", encoding="utf-8") as f_shortlist:

    results_writer = csv.writer(f_results)
    shortlist_writer = csv.writer(f_shortlist)

    results_writer.writerow(["Job Title", "Candidate Name", "Email", "Match Score", "Explanation"])
    shortlist_writer.writerow(["Job Title", "Candidate Name", "Email", "Match Score", "Explanation"])

    for i, (resume_filename, resume_text) in enumerate(resumes.items()):
        if i >= 2: break 

        print(f"\n📄 Matching resume: {resume_filename}")

        for job in jobs:
            job_title = job.get("Job Title", "Unknown Title")
            job_description = job.get("Job Description", "")

            result = evaluate_applicant_for_job(resume_filename, resume_text, job_title, job_description)

            results_writer.writerow([
                result["job_title"],
                result["name"],
                result["email"],
                result["score"],
                result["explanation"]
            ])

            if result["score"] >= 80:
                shortlist_writer.writerow([
                    result["job_title"],
                    result["name"],
                    result["email"],
                    result["score"],
                    result["explanation"]
                ])
                print(f"🏆 Shortlisted {result['name']} for {result['job_title']} (Score: {result['score']})")

print("\n✅ All resumes matched against all jobs successfully!")
