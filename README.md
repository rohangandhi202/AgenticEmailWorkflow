# 🤖 AgenticEmailWorkflow

An autonomous AI agent that tracks job applications by monitoring Gmail, 
classifying recruiter emails using Claude AI, and delivering weekly 
pipeline summaries — all without any manual data entry.

## 💡 Overview

Job searching generates a lot of email. This agent automatically:
- Detects incoming recruiter emails via Gmail label triggers
- Uses Claude AI to classify the email and extract structured data
- Creates or updates rows in a Google Sheet tracker autonomously
- Sends a weekly AI-generated digest every Sunday summarizing pipeline status

## 🏗️ Architecture
```
Gmail (Job Confirmation label)
     ↓
n8n Workflow 1 — Email Classifier
     ↓
Claude API — Extracts company, job title, status, notes
     ↓
Google Sheets — Creates new row or updates existing row
```
```
Schedule Trigger (Every Sunday)
     ↓
n8n Workflow 2 — Weekly Digest
     ↓
Claude API — Generates pipeline summary
     ↓
Gmail — Sends formatted HTML digest email
```

See `docs/architecture.md` for full node-by-node breakdown.

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| n8n (cloud) | Workflow orchestration |
| Claude API (Anthropic) | Email classification & digest generation |
| Google Sheets | Application data store |
| Gmail | Email trigger & digest delivery |
| Python | Local prompt testing |

## 📁 Project Structure
```
AgenticEmailWorkflow/
├── workflows/
│   ├── email_classifier.json     # n8n Workflow 1 export
│   └── weekly_digest.json        # n8n Workflow 2 export
├── prompts/
│   ├── email_classifier.md       # Claude prompt — email classifier
│   └── weekly_digest.md          # Claude prompt — weekly digest
├── scripts/
│   └── test_claude.py            # Local Claude API prompt tester
├── docs/
│   └── architecture.md           # Full system architecture
├── .env.example                  # Environment variable template
└── README.md
```

## 🔄 Workflow 1 — Email Classifier

**Trigger:** Email receives "Job Confirmation" Gmail label

**Logic:**
1. Extracts email subject, sender, body, and date
2. Sends to Claude with structured extraction prompt
3. Searches Google Sheet for existing Company + Job Title match
4. If match found → updates Status, Notes, Update Date
5. If no match → creates new row with all extracted fields
6. Unrecognizable emails → written as "Needs Review" for manual review

**Extracted Fields:**
- Company, Job Title, Application Link
- Status (`Submitted` / `Interview` / `Assessment` / `Rejected` / `Needs Review`)
- Notes (one-sentence summary)
- Email Date

## 📊 Workflow 2 — Weekly Digest

**Trigger:** Every Sunday at 9:00 PM

**Logic:**
1. Reads all rows from Google Sheets tracker
2. Sends full dataset to Claude for analysis
3. Claude generates structured digest with overview, attention items, recent activity, and next steps
4. Digest is converted from Markdown to HTML
5. Sent to personal Gmail as formatted email

## 🚀 Setup

### Prerequisites
- n8n cloud account (free tier)
- Anthropic API key
- Google account (Sheets + Gmail)

### Environment Variables
Copy `.env.example` to `.env` and fill in your values:
```
ANTHROPIC_API_KEY=your_key_here
GOOGLE_SHEET_ID=your_sheet_id_here
```

### Google Sheet Structure
Create a sheet with these exact column headers:
```
Submitted Date | Company | Job Title | Link To Application | Status | Notes | Update Date
```

### n8n Setup
1. Import `workflows/email_classifier.json` into n8n
2. Import `workflows/weekly_digest.json` into n8n
3. Reconnect credentials (Google Sheets, Gmail, Anthropic) in each node
4. Create a Gmail label called `Job Confirmation`
5. Activate both workflows

### Testing Prompts Locally
```bash
pip install anthropic python-dotenv
python scripts/test_claude.py
```