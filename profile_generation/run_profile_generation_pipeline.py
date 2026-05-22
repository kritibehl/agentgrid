import json
from pathlib import Path
from datetime import datetime, timezone

from profile_generation.candidate_profile_generator import generate_candidate_profile
from profile_generation.job_profile_generator import generate_job_profile
from profile_generation.profile_quality_validator import validate_profile
from profile_generation.privacy_redaction import redact_profile


SAMPLE_INPUT = {
    "candidate": {
        "candidate_id": "cand_001",
        "skills": ["Python", "FastAPI", "RAG", "Python", "Redis"],
        "job_history": [
            {"title": "Software Engineer", "focus": "backend APIs and automation"},
            {"title": "AI Support Engineer", "focus": "GenAI evaluation workflows"}
        ],
        "resume_text": "Kriti built Python FastAPI workflows, Redis queues, RAG evaluation gates, and support automation. Contact: kriti@example.com"
    },
    "job": {
        "job_id": "job_001",
        "title": "GenAI Profile Generation Engineer",
        "known_skills": ["Python", "FastAPI", "RAG", "Redis", "Responsible AI", "Evaluation"],
        "job_description": "Build profile generation services using Python, evaluation workflows, Responsible AI checks, and downstream matching quality signals."
    }
}


def match_summary(candidate_profile, job_profile) -> dict:
    candidate_skills = set(candidate_profile.get("normalized_skills", []))
    required_skills = set(job_profile.get("required_skills", []))

    overlap = sorted(candidate_skills & required_skills)
    missing = sorted(required_skills - candidate_skills)

    readiness = len(overlap) / max(1, len(required_skills))

    return {
        "overlap_skills": overlap,
        "missing_skills": missing,
        "downstream_match_score": round(readiness, 2),
        "match_readiness": readiness >= 0.5,
    }


def run_pipeline(raw=SAMPLE_INPUT):
    candidate_profile = generate_candidate_profile(raw["candidate"])
    job_profile = generate_job_profile(raw["job"])

    candidate_source = " ".join([
        raw["candidate"].get("resume_text", ""),
        " ".join(raw["candidate"].get("skills", [])),
    ])

    job_source = " ".join([
        raw["job"].get("job_description", ""),
        " ".join(raw["job"].get("known_skills", [])),
    ])

    candidate_validation = validate_profile(candidate_profile, candidate_source)
    job_validation = validate_profile(job_profile, job_source)

    redacted_candidate = redact_profile(candidate_profile)
    redacted_job = redact_profile(job_profile)

    matching = match_summary(candidate_profile, job_profile)

    audit = {
        "pipeline": "profile_generation",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stages": [
            "ingestion",
            "normalization",
            "profile_generation",
            "hallucination_checks",
            "unsupported_detail_checks",
            "privacy_redaction",
            "quality_scoring",
            "audit_log",
            "downstream_matching_summary"
        ],
        "candidate_profile": redacted_candidate["profile"],
        "job_profile": redacted_job["profile"],
        "candidate_quality": candidate_validation,
        "job_quality": job_validation,
        "privacy_risk": redacted_candidate["privacy_risk"] or redacted_job["privacy_risk"],
        "matching_feedback": matching,
    }

    Path("profile_generation/generation_audit_log.json").write_text(json.dumps(audit, indent=2))
    Path("profile_generation/matching_feedback_report.json").write_text(json.dumps(matching, indent=2))

    return audit


if __name__ == "__main__":
    print(json.dumps(run_pipeline(), indent=2))
