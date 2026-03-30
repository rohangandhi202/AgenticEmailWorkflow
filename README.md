# 🤖 AI Job Application Tracker Agent

An agentic workflow system that automatically classifies recruiter emails 
and delivers weekly AI-generated summaries of your job search pipeline.

## Tech Stack
- **n8n** — Workflow orchestration
- **Claude API (Anthropic)** — Email classification & digest generation  
- **Google Sheets** — Application data store
- **Gmail** — Email trigger & digest delivery

## Workflows
1. **Email Classifier** — Triggered on incoming recruiter emails. 
   Uses Claude to extract company, job title, status, and sentiment. 
   Writes structured data to Google Sheets automatically.

2. **Weekly Digest** — Runs every Sunday. Reads the full 
   application sheet, generates an AI summary of pipeline 
   status and suggested next steps, and emails it to you.

## Architecture
See `docs/architecture.md` for the full system design.

## Prompts
Claude prompt templates are in the `/prompts` directory.

## Status
🚧 In progress