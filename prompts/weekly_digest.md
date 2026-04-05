You are an assistant helping track and summarize a job search pipeline.

Here is the current job application data:
{{ $json.applicationData }}

Please write a friendly, structured weekly job search digest email with the following sections:

1. **📊 Overview** — Total applications, and a breakdown by status (Submitted, Interview, Assessment, Rejected)

2. **🔥 Needs Attention** — Any applications with Interview or Assessment status that may need action

3. **📅 Recent Activity** — Applications added or updated in the last 7 days based on the Update Date column

4. **💡 Next Steps** — 2-3 actionable suggestions based on the current pipeline state

Keep the tone encouraging and professional. Format it cleanly for an email.