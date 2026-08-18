"""
Ye file define karti hai ki ek "Complaint" ka data structure kaisa hoga.
Pydantic isko automatically validate karega - agar AI ne galat type ka
data bheja (jaise number ki jagah text), to yahi pakad lega.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import date


# Enum = fixed set of allowed values (dropdown jaisa)
class SeverityLevel(str, Enum):
    critical = "Critical"
    major = "Major"
    minor = "Minor"


class PriorityLevel(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class ComplaintType(str, Enum):
    packaging = "Packaging Issue"
    quality_defect = "Quality Defect"
    delivery = "Delivery Issue"
    contamination = "Contamination"
    labeling = "Labeling Error"
    other = "Other"


# Ye woh structure hai jo AI extraction ke baad return hoga
# Saari fields Optional hain kyunki AI ko document me sab kuch nahi milega
class ExtractedComplaintData(BaseModel):
    complaint_source: Optional[str] = Field(None, description="Email, phone, portal, etc.")
    customer_name: Optional[str] = None

    product_name: Optional[str] = None
    product_strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None  # string rakha hai kyunki AI se date format vary karta hai
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None

    complaint_type: Optional[ComplaintType] = None
    complaint_date: Optional[str] = None
    complaint_description: Optional[str] = None

    initial_severity: Optional[SeverityLevel] = None
    priority: Optional[PriorityLevel] = None

    # Bonus feature ke liye - AI apna reasoning bhi bata sakta hai
    ai_confidence_notes: Optional[str] = Field(
        None, description="AI's notes on what it wasn't sure about"
    )


# Ye full complaint jo database me save hogi (extracted data + extra fields)
class ComplaintCreate(ExtractedComplaintData):
    pass


class ComplaintResponse(ExtractedComplaintData):
    id: int
    status: str = "Pending Triage"

    class Config:
        from_attributes = True  # SQLAlchemy model se convert karne ke liye