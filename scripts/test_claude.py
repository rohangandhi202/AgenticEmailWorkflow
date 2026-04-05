import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

# Sample test email — swap this out to test different scenarios
TEST_EMAIL = {
    "subject": "Uber Careers: Thank you for your application for Software Engineer",
    "from": "noreply@uber.com",
    "snippet": "Hey Rohan, Thank you for applying to Uber! We have received your application for the Software Engineer opportunity. What happens next? We will review your application and contact you if there is a good fit.",
    "date": "1775314277000"
}

def test_email_classifier(email: dict) -> dict:
    client = anthropic.Anthropic()
    
    prompt = f"""You are an assistant helping track job applications.
Analyze the following email and return a JSON object only, no explanation, no markdown.

Email Subject: {email['subject']}
Email From: {email['from']}
Email Body: {email['snippet']}
Email Date: {email['date']}

Return this exact JSON structure:
{{
  "email_type": "new_application" or "follow_up",
  "company": "",
  "job_title": "",
  "application_link": "",
  "status": "Submitted" or "Rejected" or "Assessment" or "Interview" or "Needs Review",
  "notes": "",
  "email_date": ""
}}

Rules:
- If this is a new application confirmation, set email_type to "new_application" and status to "Submitted"
- If this is a follow-up (rejection, interview invite, assessment), set email_type to "follow_up"
- If you cannot confidently identify the company or job title, set status to "Needs Review"
- Keep notes to one sentence max
- Return ONLY the JSON, nothing else"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = message.content[0].text
    parsed = json.loads(raw)
    return parsed


if __name__ == "__main__":
    print("Testing Email Classifier Prompt...\n")
    print(f"Input Email: {TEST_EMAIL['subject']}\n")
    
    result = test_email_classifier(TEST_EMAIL)
    
    print("Claude Output:")
    print(json.dumps(result, indent=2))