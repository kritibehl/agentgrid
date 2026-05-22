import re
from typing import Dict, Tuple


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\-\s().]{8,}\d)")


def redact_text(text: str) -> Tuple[str, bool]:
    privacy_risk = bool(EMAIL_RE.search(text) or PHONE_RE.search(text))
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text, privacy_risk


def redact_profile(profile: Dict) -> Dict:
    redacted = dict(profile)
    privacy_risk = False

    for field in ["raw_resume_excerpt", "job_description_excerpt", "summary"]:
        if field in redacted and isinstance(redacted[field], str):
            redacted_value, risk = redact_text(redacted[field])
            redacted[field] = redacted_value
            privacy_risk = privacy_risk or risk

    return {
        "profile": redacted,
        "privacy_risk": privacy_risk,
    }
