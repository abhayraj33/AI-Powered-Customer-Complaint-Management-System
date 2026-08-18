"""
Ye file hamara LangGraph "AI Agent" hai.

Simple words me: Ye ek pipeline hai jisme complaint text jaata hai,
aur structured data (JSON) bahar aata hai - jaise humne Pydantic
models me define kiya tha.

Flow:
  1. Raw text/document aata hai
  2. Node 1: LLM se structured fields extract karte hain
  3. Node 2: LLM se severity/risk classify karte hain
  4. Final state return hota hai (jo frontend ko jayega)
"""

import json
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from groq import Groq

from app.core.config import settings

# Groq client banate hain - isse hum LLM ko call karenge
client = Groq(api_key=settings.GROQ_API_KEY)


# ============================================================
# STATE: Ye woh "data packet" hai jo ek node se doosre node
# tak travel karta hai. Jaisे-jaise flow aage badhta hai,
# ye state update hoti rehti hai.
# ============================================================
class ComplaintState(TypedDict):
    raw_text: str                    # input: user ne jo text/document diya
    extracted_data: Optional[dict]   # step 1 ke baad fill hoga
    risk_assessment: Optional[dict]  # step 2 ke baad fill hoga
    error: Optional[str]


# ============================================================
# HELPER: Groq LLM ko call karne ka function
# ============================================================
def call_llm(prompt: str, model: str = None) -> str:
    """LLM ko prompt bhejta hai aur uska text response wapas deta hai."""
    model_name = model or settings.EXTRACTION_MODEL
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,  # low temperature = zyada consistent/factual output
        response_format={"type": "json_object"},  # Groq ko force karo JSON dene ke liye
    )
    return response.choices[0].message.content


# ============================================================
# NODE 1: Extraction - complaint text se structured fields nikalna
# ============================================================
def extract_complaint_info(state: ComplaintState) -> ComplaintState:
    prompt = f"""
You are a pharmaceutical quality assurance assistant. Extract structured
information from the following customer complaint text.

Return ONLY a valid JSON object with these exact keys (use null if not found):
- complaint_source (e.g. "Email", "Phone", "Customer Portal")
- customer_name
- product_name
- product_strength
- batch_number
- manufacturing_date
- expiry_date
- quantity_affected
- complaint_type (one of: "Packaging Issue", "Quality Defect", "Delivery Issue", "Contamination", "Labeling Error", "Other")
- complaint_date
- complaint_description (a clean summary of the actual issue)

Complaint text:
\"\"\"
{state['raw_text']}
\"\"\"

Return ONLY the JSON object, no other text.
"""
    try:
        result = call_llm(prompt)
        extracted = json.loads(result)
        state["extracted_data"] = extracted
    except Exception as e:
        state["error"] = f"Extraction failed: {str(e)}"
        state["extracted_data"] = {}

    return state


# ============================================================
# NODE 2: Risk/Severity Classification
# ============================================================
def classify_risk(state: ComplaintState) -> ComplaintState:
    extracted = state.get("extracted_data", {})
    description = extracted.get("complaint_description", state["raw_text"])

    prompt = f"""
You are a pharmaceutical QA risk assessor. Based on this complaint description,
classify the severity and priority.

Complaint: "{description}"

Guidelines:
- Critical: patient safety risk, contamination, wrong drug/dosage
- Major: quality defect but no immediate safety risk (e.g. packaging damage, labeling error)
- Minor: cosmetic/minor issue with no functional impact

Return ONLY a valid JSON object with these keys:
- initial_severity (one of: "Critical", "Major", "Minor")
- priority (one of: "High", "Medium", "Low")
- reasoning (one short sentence explaining why)
"""
    try:
        result = call_llm(prompt)
        risk_data = json.loads(result)
        state["risk_assessment"] = risk_data
    except Exception as e:
        state["error"] = (state.get("error") or "") + f" | Risk classification failed: {str(e)}"
        state["risk_assessment"] = {}

    return state


# ============================================================
# GRAPH: Nodes ko jodkar ek workflow banate hain
# ============================================================
def build_complaint_graph():
    graph = StateGraph(ComplaintState)

    # Nodes add karo
    graph.add_node("extract_info", extract_complaint_info)
    graph.add_node("classify_risk", classify_risk)

    # Flow define karo: extract -> classify -> end
    graph.set_entry_point("extract_info")
    graph.add_edge("extract_info", "classify_risk")
    graph.add_edge("classify_risk", END)

    return graph.compile()


# Ye compiled graph hai jo API endpoint use karega
complaint_graph = build_complaint_graph()


# ============================================================
# MAIN FUNCTION: API se yehi call hoga
# ============================================================
def process_complaint_text(raw_text: str) -> dict:
    """
    Ye function poore LangGraph workflow ko run karta hai
    aur final combined result deta hai.
    """
    initial_state: ComplaintState = {
        "raw_text": raw_text,
        "extracted_data": None,
        "risk_assessment": None,
        "error": None,
    }

    final_state = complaint_graph.invoke(initial_state)

    # Extraction aur risk assessment ko combine karke ek response banate hain
    combined = {
        **(final_state.get("extracted_data") or {}),
        "initial_severity": (final_state.get("risk_assessment") or {}).get("initial_severity"),
        "priority": (final_state.get("risk_assessment") or {}).get("priority"),
        "ai_confidence_notes": (final_state.get("risk_assessment") or {}).get("reasoning"),
    }

    if final_state.get("error"):
        combined["_error"] = final_state["error"]

    return combined