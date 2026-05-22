from typing import Dict, List


def normalize_skills(skills: List[str]) -> List[str]:
    return sorted({skill.strip().lower() for skill in skills if skill and skill.strip()})


def generate_candidate_profile(raw: Dict) -> Dict:
    resume_text = raw.get("resume_text", "")
    skills = normalize_skills(raw.get("skills", []))
    job_history = raw.get("job_history", [])

    inferred_summary = "Candidate profile generated from provided skills, resume text, and job history."

    return {
        "profile_type": "candidate",
        "candidate_id": raw.get("candidate_id", "unknown_candidate"),
        "normalized_skills": skills,
        "experience_count": len(job_history),
        "job_history": job_history,
        "summary": inferred_summary,
        "source_fields_used": ["skills", "resume_text", "job_history"],
        "raw_resume_excerpt": resume_text[:240],
        "generated_claims": [
            f"Has experience with {skill}" for skill in skills[:5]
        ],
    }
