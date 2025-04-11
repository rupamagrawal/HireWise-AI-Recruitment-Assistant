import subprocess
import sys

def run_script(script_path, message):
    print(f"\n🔹 {message}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run {script_path}: {e}")
        exit(1)

if __name__ == "__main__":
    steps = [
        ("scripts/extract_pdfs.py", "Extracting resume PDFs..."),
        ("scripts/load_jobs.py", "Loading job descriptions..."),
        ("scripts/run_matching.py", "Matching candidates to jobs...")
    ]

    for script, message in steps:
        run_script(script, message)

    print("\n✅ All steps completed successfully!")
