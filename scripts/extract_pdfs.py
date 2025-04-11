import fitz  # PyMuPDF
import os
import json

def extract_resume_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

resume_folder = "data/resumes"
parsed = {}

if not os.path.exists(resume_folder):
    raise FileNotFoundError("❌ Resume folder not found: data/resumes")

for filename in os.listdir(resume_folder):
    if filename.endswith(".pdf"):
        text = extract_resume_text(os.path.join(resume_folder, filename))
        parsed[filename] = text

os.makedirs("parsed_data", exist_ok=True)
with open("parsed_data/parsed_resumes.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2)

print("✅ Resumes extracted successfully!")
