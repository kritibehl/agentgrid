from typing import Dict, List


REQUIRED_CANDIDATE_FIELDS = ["candidate_id", "normalized_skills", "job_history", "summary"]
REQUIRED_JOB_FIELDS = ["job_id", "title", "required_skills"]


def detect_unsupported_claims(profile: Dict, source_text: str) -> List[str]:
    unsupported = []
    lower_source = source_text.lower()

    for claim in profile.get("generated_claims", []):
        tokens = [
            token.lower().strip(".,")
            for token in claim.split()
            if len(token.strip(".,").lower()) > 3
        ]
        if not any(token in lower_source for token in tokens):
            unsupported.append(claim)

    return unsupported


def validate_profile(profile: Dict, source_text: str) -> Dict:
    profile_type = profile.get("profile_type")
    required = REQUIRED_CANDIDATE_FIELDS if profile_type == "candidate" else REQUIRED_JOB_FIELDS

    missing_fields = [
        field for field in required
        if field not in profile or profile.get(field) in (None, "", [])
    ]

    unsupported_claims = detect_unsupported_claims(profile, source_text)
    hallucination_detected = len(unsupported_claims) > 0

    score = 1.0
    score -= 0.15 * len(missing_fields)
    score -= 0.20 * len(unsupported_claims)
    score = max(0.0, round(score, 2))

    match_readiness = (
        score >= 0.75
        and not hallucination_detected
        and len(missing_fields) == 0
    )

    return {
        "profile_quality_score": score,
        "missing_fields": missing_fields,
        "hallucination_detected": hallucination_detected,
        "unsupported_claims": unsupported_claims,
        "match_readiness": match_readiness,
    }
