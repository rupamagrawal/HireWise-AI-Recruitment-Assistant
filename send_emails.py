import csv
import os
import smtplib
from dotenv import load_dotenv
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Email subject
SUBJECT = "🎉 Interview Invitation: You're Shortlisted for the Role!"

# Generate interview date and time (tomorrow at 11:00 AM)
interview_datetime = datetime.now() + timedelta(days=1)
formatted_date = interview_datetime.strftime("%A, %d %B %Y")
formatted_time = "11:00 AM"

# Email body template
BODY_TEMPLATE = """
Hi {name},

We’re excited to let you know that you’ve been **shortlisted for the role of {job_title}** 🎯

Your resume stood out for its alignment with the job’s requirements — your background, experience, and skill set match well with what we’re looking for in this role.

📅 **Interview Details:**  
Date: {date}  
Time: {time}  
Mode: Online or Offline (depending on your preference)

Please reply to this email to confirm your availability and preferred mode.

We look forward to connecting with you!

Warm regards,  
Recruitment Team 🤖
"""

# Send email to all shortlisted candidates
with open("output/shortlisted_candidates.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["Candidate Name"]
        email = row["Email"]
        job_title = row["Job Title"]

        # Prepare the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = SUBJECT

        # Fill in the email body
        body = BODY_TEMPLATE.format(
            name=name,
            job_title=job_title,
            date=formatted_date,
            time=formatted_time
        )
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f"✅ Email sent to {name} ({email})")
        except Exception as e:
            print(f"❌ Failed to send email to {name} ({email}): {e}")
