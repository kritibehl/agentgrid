def search_knowledge_base(query):
    return {"docs": ["runbook: retrieval miss", "policy: human review required"], "retrieval_hit": True}

def summarize_issue(text):
    return {"summary": text[:120], "risk": "medium"}

def classify_priority(summary):
    return {"priority": "high" if "unsafe" in summary.lower() else "medium"}

def generate_handoff_note(summary, priority):
    return {"handoff_note": f"Priority {priority}: {summary}"}

def validate_claim(claim, docs):
    grounded = any(word in " ".join(docs).lower() for word in claim.lower().split())
    return {"grounded": grounded, "human_review_required": not grounded}
