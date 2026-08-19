"""
Ye file define karti hai ki ek "Complaint" ka data structure kaisa hoga.
Pydantic isko automatically validate karega - agar AI ne galat type ka
data bheja (jaise number ki jagah text), to yahi pakad lega.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
from datetime import date


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


class ExtractedComplaintData(BaseModel):
    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None

    product_name: Optional[str] = None
    product_strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None

    complaint_type: Optional[ComplaintType] = None
    complaint_date: Optional[str] = None
    complaint_description: Optional[str] = None

    initial_severity: Optional[SeverityLevel] = None
    priority: Optional[PriorityLevel] = None

    ai_confidence_notes: Optional[str] = Field(
        None, description="AI's notes on what it wasn't sure about"
    )
    ai_summary: Optional[str] = Field(
        None, description="One-line AI-generated summary for quick triage"
    )

    # Ye validator ensure karta hai ki agar AI number bhej de (jaise 30),
    # to use automatically string me convert kar diya jaye ("30")
    @field_validator('quantity_affected', 'batch_number', 'manufacturing_date',
                      'expiry_date', 'complaint_date', mode='before')
    @classmethod
    def convert_to_string(cls, v):
        if v is None:
            return v
        return str(v)


class ComplaintCreate(ExtractedComplaintData):
    pass


class ComplaintResponse(ExtractedComplaintData):
    id: int
    status: str = "Pending Triage"

    class Config:
        from_attributes = True