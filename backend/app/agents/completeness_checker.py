"""
BONUS FEATURE: Complaint Completeness Checker

Ye check karta hai ki complaint ke zaroori (critical) fields fill hain ya nahi.
Agar kuch missing hai, to AI se customer ko poochne wale specific
follow-up questions bhi generate karwata hai.

Note: Completeness check khud AI use nahi karta (fast, reliable, free) -
sirf jab fields missing hoti hain tab AI follow-up questions banane
ke liye call hota hai.
"""

import json
from app.agents.complaint_agent import call_llm
from app.core.config import settings

# Ye fields QMS (Quality Management System) ke hisaab se
# ek complaint record ko "complete" maane jaane ke liye zaroori hain
CRITICAL_FIELDS = {
    "customer_name": "Customer Name",
    "product_name": "Product Name",
    "batch_number": "Batch/Lot Number",
    "complaint_description": "Complaint Description",
    "initial_severity": "Initial Severity",
}

RECOMMENDED_FIELDS = {
    "manufacturing_date": "Manufacturing Date",
    "expiry_date": "Expiry Date",
    "quantity_affected": "Quantity Affected",
    "complaint_type": "Complaint Type",
}


def check_completeness(complaint_data: dict) -> dict:
    """
    Complaint data leke check karta hai kitna 'complete' hai.
    Returns: completeness score, missing critical/recommended fields,
    aur (agar zaroorat ho) AI-generated follow-up questions.
    """
    missing_critical = []
    missing_recommended = []

    for field_key, field_label in CRITICAL_FIELDS.items():
        value = complaint_data.get(field_key)
        if not value or (isinstance(value, str) and not value.strip()):
            missing_critical.append(field_label)

    for field_key, field_label in RECOMMENDED_FIELDS.items():
        value = complaint_data.get(field_key)
        if not value or (isinstance(value, str) and not value.strip()):
            missing_recommended.append(field_label)

    total_fields = len(CRITICAL_FIELDS) + len(RECOMMENDED_FIELDS)
    filled_fields = total_fields - len(missing_critical) - len(missing_recommended)
    completeness_score = round((filled_fields / total_fields) * 100)

    result = {
        "completeness_score": completeness_score,
        "is_complete": len(missing_critical) == 0,
        "missing_critical_fields": missing_critical,
        "missing_recommended_fields": missing_recommended,
        "follow_up_questions": [],
    }

    # Agar kuch bhi missing hai, AI se customer ke liye follow-up
    # questions generate karwao (sirf tabhi AI call hoti hai)
    all_missing = missing_critical + missing_recommended
    if all_missing:
        result["follow_up_questions"] = _generate_follow_up_questions(all_missing)

    return result


def _generate_follow_up_questions(missing_fields: list) -> list:
    """AI se customer ko poochne wale polite, specific questions banwao."""
    prompt = f"""
You are a pharmaceutical QA complaint intake assistant. The following
information is missing from a customer complaint: {', '.join(missing_fields)}

Generate short, polite follow-up questions to ask the customer to get
this missing information. One question per missing field.

Return ONLY a valid JSON object with one key:
- questions (a list of strings, one question per missing field)
"""
    try:
        result = call_llm(prompt, model=settings.EXTRACTION_MODEL)
        data = json.loads(result)
        return data.get("questions", [])
    except Exception:
        # Agar AI call fail ho jaye, to bhi basic fallback questions de do
        return [f"Could you please provide the {field}?" for field in missing_fields]