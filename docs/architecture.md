# 🏗️ System Architecture

## Overview

AgenticEmailWorkflow is a two-workflow agentic system built on n8n that 
automates job application tracking using Gmail, Claude AI, and Google Sheets.

---

## Workflow 1 — Email Classifier

**Trigger:** Gmail label "Job Confirmation" (polls every 5 minutes)

### Node Breakdown

| # | Node | Type | Purpose |
|---|------|------|---------|
| 1 | Gmail Trigger | Trigger | Fires when email receives "Job Confirmation" label |
| 2 | Edit Fields | Transform | Extracts emailSubject, emailFrom, emailSnippet, emailDate |
| 3 | Message a Model | Anthropic | Sends email data to Claude, returns structured JSON |
| 4 | Code in JavaScript | Code | Parses Claude's JSON response, formats date |
| 5 | Get Row(s) in Sheet | Google Sheets | Searches for existing row by Company + Job Title |
| 6 | Merge | Merge | Combines Claude's parsed data with sheet search result |
| 7 | IF | Logic | Routes based on whether a matching row was found |
| 8a | Update Row | Google Sheets | Updates Status, Notes, Update Date on existing row |
| 8b | Append Row | Google Sheets | Creates new row for new application |

### Decision Logic
```
Email arrives with "Job Confirmation" label
          ↓
Claude extracts: company, job_title, status, notes, email_date
          ↓
Search Google Sheet for matching Company + Job Title
          ↓
Match found?
├── YES (row_number exists) → Update existing row
│         Status, Notes, Update Date
│
└── NO (row_number empty) → Append new row
          All fields written
          
Edge case: Claude can't parse → status set to "Needs Review"
```

### Claude Prompt — Email Classifier
See `prompts/email_classifier.md`

### Status Values

| Status | Meaning |
|--------|---------|
| Submitted | Application confirmation received |
| Interview | Interview invite received |
| Assessment | Online assessment / take-home received |
| Rejected | Rejection email received |
| Needs Review | Claude could not confidently classify |

---

## Workflow 2 — Weekly Digest

**Trigger:** Schedule — Every Sunday at 9:00 PM

### Node Breakdown

| # | Node | Type | Purpose |
|---|------|------|---------|
| 1 | Schedule Trigger | Trigger | Fires every Sunday at 9:00 PM |
| 2 | Get Many Rows | Google Sheets | Reads all rows from application tracker |
| 3 | Code in JavaScript | Code | Converts row data to JSON string for Claude |
| 4 | Message a Model | Anthropic | Generates structured digest from application data |
| 5 | Code in JavaScript | Code | Converts Claude's Markdown response to HTML |
| 6 | Gmail | Gmail | Sends formatted digest email to personal inbox |

### Digest Structure

Claude generates a digest with four sections:

1. **📊 Overview** — Total applications and status breakdown
2. **🔥 Needs Attention** — Interview/Assessment items requiring action
3. **📅 Recent Activity** — Applications from the last 7 days
4. **💡 Next Steps** — 2-3 actionable suggestions

### Claude Prompt — Weekly Digest
See `prompts/weekly_digest.md`

---

## Google Sheet Structure

| Column | Populated By |
|--------|-------------|
| Submitted Date | Claude (from email timestamp) |
| Company | Claude (extracted from email) |
| Job Title | Claude (extracted from email) |
| Link To Application | Claude (extracted from email) |
| Status | Claude (classified) |
| Notes | Claude (one-sentence summary) |
| Update Date | Claude (timestamp of latest email) |

---

## Design Decisions

**Why n8n over Zapier?**
n8n offers more flexibility for conditional logic, custom code nodes, 
and multi-input merging — all of which this workflow requires. Free 
cloud tier is sufficient for this use case.

**Why Google Sheets over a database?**
Zero setup, free, and human-readable. For a personal job tracker with 
under 500 rows, Sheets is more practical than spinning up a database.

**Why snippet instead of full email body?**
Gmail's full body requires recursive MIME parsing. The snippet 
(first ~200 characters) contains sufficient context for Claude to 
classify the email type and extract key fields reliably.

**Why Merge node instead of referencing upstream nodes?**
When Get Row returns empty, n8n can stop data flow unpredictably. 
The Merge node guarantees Claude's parsed data is always available 
to both the Append and Update branches regardless of sheet search result.