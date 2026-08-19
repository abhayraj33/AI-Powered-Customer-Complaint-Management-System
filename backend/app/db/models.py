"""
Ye file define karti hai ki database me actual table kaisi dikhegi.
Pydantic (jo humne pehle banaya) API validation ke liye hai,
ye SQLAlchemy model DATABASE me store karne ke liye hai.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    # Origin & Customer
    complaint_source = Column(String(100), nullable=True)
    customer_name = Column(String(200), nullable=True)

    # Product & Batch
    product_name = Column(String(200), nullable=True)
    product_strength = Column(String(100), nullable=True)
    batch_number = Column(String(100), nullable=True)
    manufacturing_date = Column(String(50), nullable=True)
    expiry_date = Column(String(50), nullable=True)
    quantity_affected = Column(String(100), nullable=True)

    # Complaint details
    complaint_type = Column(String(100), nullable=True)
    complaint_date = Column(String(50), nullable=True)
    complaint_description = Column(Text, nullable=True)

    # Assessment
    initial_severity = Column(String(50), nullable=True)
    priority = Column(String(50), nullable=True)
    ai_confidence_notes = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)

    # Status tracking
    status = Column(String(50), default="Pending Triage")

    # Timestamps - automatically set hote hain
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())