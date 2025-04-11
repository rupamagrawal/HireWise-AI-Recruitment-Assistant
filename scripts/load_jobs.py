import pandas as pd
import json
import os

file_path = "data/job_descriptions.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError("❌ job_descriptions.csv not found!")

jobs_df = pd.read_csv(file_path, encoding='ISO-8859-1')
required_columns = ["Job Title", "Job Description"]
for col in required_columns:
    if col not in jobs_df.columns:
        raise ValueError(f"❌ Missing column in CSV: {col}")

jobs = jobs_df.to_dict(orient="records")
os.makedirs("parsed_data", exist_ok=True)

with open("parsed_data/parsed_jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print("✅ Job descriptions loaded successfully!")
