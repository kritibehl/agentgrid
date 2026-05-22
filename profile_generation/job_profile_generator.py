from typing import Dict, List


def extract_required_skills(job_description: str, known_skills: List[str]) -> List[str]:
    text = job_description.lower()
    return sorted({skill.lower() for skill in known_skills if skill.lower() in text})


def generate_job_profile(raw: Dict) -> Dict:
    jd = raw.get("job_description", "")
    known_skills = raw.get("known_skills", [])

    required_skills = extract_required_skills(jd, known_skills)

    return {
        "profile_type": "job",
        "job_id": raw.get("job_id", "unknown_job"),
        "title": raw.get("title", "unknown_title"),
        "required_skills": required_skills,
        "source_fields_used": ["job_description", "title", "known_skills"],
        "job_description_excerpt": jd[:300],
        "generated_claims": [
            f"Role requires {skill}" for skill in required_skills
        ],
    }
