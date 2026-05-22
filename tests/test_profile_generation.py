from profile_generation.run_profile_generation_pipeline import run_pipeline
from profile_generation.privacy_redaction import redact_text


def test_profile_pipeline_outputs_quality_and_matching():
    result = run_pipeline()

    assert "candidate_quality" in result
    assert "job_quality" in result
    assert "matching_feedback" in result
    assert "profile_quality_score" in result["candidate_quality"]
    assert "match_readiness" in result["matching_feedback"]


def test_privacy_redaction_detects_email():
    redacted, risk = redact_text("Contact me at person@example.com")

    assert risk is True
    assert "[REDACTED_EMAIL]" in redacted
