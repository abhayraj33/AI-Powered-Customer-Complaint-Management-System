"""
API endpoints - ye woh URLs hain jo frontend call karega.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.agents.completeness_checker import check_completeness
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.agents.complaint_agent import process_complaint_text
from app.models.complaint import ExtractedComplaintData, ComplaintResponse
from app.db.session import get_db
from app.db.models import Complaint

router = APIRouter(prefix="/api/complaints", tags=["complaints"])


# Jab user text paste karta hai (email/complaint text)
class TextExtractionRequest(BaseModel):
    text: str


@router.post("/extract-from-text", response_model=dict)
def extract_from_text(request: TextExtractionRequest):
    """
    User raw complaint text bhejta hai -> AI structured data extract
    karke wapas bhejta hai -> frontend form auto-fill ho jata hai.
    """
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Complaint text too short or empty")

    result = process_complaint_text(request.text)
    return result


@router.post("/extract-from-file", response_model=dict)
async def extract_from_file(file: UploadFile = File(...)):
    """
    User PDF/DOCX/TXT upload karta hai -> pehle text nikalte hain
    file se, phir wahi extraction pipeline chalate hain.

    Note: Production-grade OCR zaroori nahi hai (assignment ke mutabik),
    isliye simple text extraction use kar rahe hain.
    """
    allowed_types = ["application/pdf", "text/plain",
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    content = await file.read()
    extracted_text = ""

    if file.content_type == "text/plain":
        extracted_text = content.decode("utf-8")

    elif file.content_type == "application/pdf":
        # Simple PDF text extraction (pypdf use karenge)
        import io
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(content))
        extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    elif "wordprocessingml" in file.content_type:
        import io
        from docx import Document
        doc = Document(io.BytesIO(content))
        extracted_text = "\n".join(p.text for p in doc.paragraphs)

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    result = process_complaint_text(extracted_text)
    return result


# ============================================================
# Save karne, list dekhne, aur single complaint fetch karne
# ke endpoints - ye actual database ke saath kaam karte hain
# ============================================================

@router.post("/", response_model=ComplaintResponse)
def save_complaint(complaint: ExtractedComplaintData, db: Session = Depends(get_db)):
    """User form ko 'Save Complaint' dabata hai -> yaha data DB me save hota hai."""
    db_complaint = Complaint(**complaint.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


@router.get("/", response_model=List[ComplaintResponse])
def list_complaints(db: Session = Depends(get_db)):
    """Dashboard ke liye - saari complaints ki list."""
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    """Ek specific complaint ki detail."""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

# ============================================================
# BONUS FEATURE: Completeness Checker
# ============================================================

@router.post("/check-completeness")
def check_complaint_completeness(complaint: ExtractedComplaintData):
    """
    Current form data leke check karta hai kitna complete hai,
    aur agar kuch missing hai to follow-up questions bhi deta hai.
    """
    result = check_completeness(complaint.model_dump())
    return result