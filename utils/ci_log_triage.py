import argparse
import os
import re
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class LogTriageResult(BaseModel):
    category: Literal["PRODUCT_BUG", "AUTOMATION_ISSUE", "INFRASTRUCTURE", "UNKNOWN"]
    root_cause_summary: str = Field(description="1-2 sentence executive summary.")
    failing_service: str = Field(description="Origin service or test harness.")
    evidence_chain: list[str] = Field(description="Chronological key events leading to failure.")
    recommended_action: str = Field(description="Remediation steps.")

def sanitize_logs(raw_text: str) -> str:
    """Masks secrets, tokens, PII, and credentials before tokenization."""
    patterns = [
        # Bearer tokens & JWTs
        (r"(Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*", r"\1[TOKEN_REDACTED]"),
        # Basic auth / base64 strings
        (r"(Basic\s+)[A-Za-z0-9+/=]{16,}", r"\1[AUTH_REDACTED]"),
        # Email addresses
        (r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL_REDACTED]"),
        # Common key/secret assignment patterns (json, headers, or logs)
        (r'(?i)(api[_-]?key|secret|password|passwd|token)["\']?\s*[:=]\s*["\']?[A-Za-z0-9\-_\.~]{8,}["\']?', 
         r'\1=[SECRET_REDACTED]'),
        # Credit Card Numbers (13-16 digits formatted or continuous)
        (r"\b(?:\d{4}[ -]?){3}\d{4}\b", "[CC_REDACTED]"),
        # IPv4 addresses (optional, helps avoid leaking internal topology)
        (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP_REDACTED]")
    ]

    sanitized = raw_text
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized

def extract_correlation_id(log_content: str) -> str | None:
    match = re.search(r"correlation_id[:=]\s*([a-zA-Z0-9\-_]+)", log_content)
    return match.group(1) if match else None

def triage(clean_logs: str) -> LogTriageResult:
    prompt = (
        "You are an expert QA triage assistant. Analyze these CI test logs.\n"
        "Determine whether the failure was caused by a PRODUCT_BUG, an AUTOMATION_ISSUE, "
        "or INFRASTRUCTURE, and summarize the root cause."
    )
    res = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": clean_logs[-8000:]}  # Guard context window
        ],
        response_format=LogTriageResult,
        temperature=0.1,
    )
    return res.choices[0].message.parsed

def write_github_summary(result: LogTriageResult, correlation_id: str | None):
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    badge_map = {
        "PRODUCT_BUG": "🚨 **Product Defect**",
        "AUTOMATION_ISSUE": "🛠️ **Automation/Test Issue**",
        "INFRASTRUCTURE": "⚙️ **Infrastructure Flake**",
        "UNKNOWN": "❓ **Unknown**"
    }

    markdown = f"""
### 🤖 AI Triage: {badge_map.get(result.category, result.category)}

* **Trace ID:** `{correlation_id or 'N/A'}`
* **Origin:** `{result.failing_service}`
* **Summary:** {result.root_cause_summary}

#### Evidence Chain
{"".join(f"- {step}\n" for step in result.evidence_chain)}

#### Recommended Fix
> {result.recommended_action}
"""
    with open(summary_path, "a") as f:
        f.write(markdown)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    with open(args.log_file, "r", errors="ignore") as f:
        raw_logs = f.read()

    # 1. Sanitize all logs first
    clean_logs = sanitize_logs(raw_logs)

    # 2. Extract correlation ID (safe to do from clean or raw logs)
    corr_id = extract_correlation_id(clean_logs)

    # 3. Analyze sanitized logs and report
    triage_result = triage(clean_logs)
    write_github_summary(triage_result, corr_id)