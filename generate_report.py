import json
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

PROMPT_FILE = "optimized_prompt_output.txt"
CONSTRAINTS_FILE = "retrieved_constraints.txt"
REQS_FILE = "last_user_requirements.json"
REPORT_FILE = "vastu_compliance_report.md"


def _read_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def _read_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Fallback report generation removed in favor of strict LLM generation


def generate_vastu_report() -> bool:
    prompt_text = _read_text(PROMPT_FILE)
    constraints_text = _read_text(CONSTRAINTS_FILE)
    reqs = _read_json(REQS_FILE)

    if not prompt_text:
        print(f"Error: {PROMPT_FILE} not found or empty.")
        return False

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Cannot generate LLM report.")
        return False

    try:
        llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
            google_api_key=api_key,
            temperature=0.2,
        )

        template = """
You are a senior architectural consultant and Vastu compliance auditor preparing a professional technical report.

Your task is to analyze a generated floor plan and produce a structured **Vastu + KPBR Compliance Report**.

The report must be professional, structured, concise but insightful, similar to a real architectural audit document.

Use the exact report structure below.

------------------------------------------------------------

# AI Vastu Compliance Report
Generated on: {current_date}

---

## 1. Project Overview
Provide a concise summary of the project using the user requirements.

Include:

• Plot Size  
• Plot Shape  
• Facing Direction  
• Floors  
• Total Built-up Area  
• Building Type  
• Requested Rooms  

Explain briefly the architectural objective of the layout.

---

## 2. Generated Floor Plan Summary
Describe the overall spatial organization.

Include:

• Entrance placement  
• Public zone layout (living / dining)  
• Service zone layout (kitchen / utilities)  
• Private zone layout (bedrooms)  
• Vertical circulation (stairs)  
• Movement flow through the house  

Explain how the spatial layout supports functionality and usability.

---

## 3. Vastu Compliance Analysis

Evaluate the placement of key rooms.

Use this evaluation structure:

Room  
Recommended Direction  
Actual Placement  
Verdict (Excellent / Good / Mixed / Non-Compliant)  
Explanation

Rooms to evaluate:

• Main Entrance  
• Living Room  
• Kitchen  
• Master Bedroom  
• Secondary Bedrooms  
• Bathrooms  
• Pooja Room  
• Staircase  

Explain briefly how each placement affects energy flow, ventilation, daylight, and spatial harmony.

---

## 4. KPBR / Building Regulation Compliance

Evaluate the layout against Kerala building rules.

Discuss:

• Front setback  
• Rear setback  
• Side setbacks  
• Minimum room sizes  
• Ventilation provisions  
• Circulation spaces  
• Parking provisions  

If exact compliance cannot be confirmed, mark as **Validation Required**.

Use bullet points for clarity.

---

## 5. Vastu Compliance Score

Provide a structured score breakdown.

Criteria:

Entrance Orientation  
Room Placement  
Bedroom Alignment  
Kitchen Placement  
Toilet Placement  
Ventilation and Natural Light  
Circulation Efficiency  
Plot Orientation

Each criterion should be scored.

Example:

Entrance Orientation – 18 / 20  
Room Placement – 20 / 25  
Bedroom Alignment – 12 / 15  
Kitchen Placement – 9 / 10  
Toilet Placement – 7 / 10  
Ventilation – 8 / 10  
Circulation – 7 / 10  
Plot Orientation – 6 / 10  

Final Score: **XX / 100**

Rating scale:

90–100 → Excellent  
75–89 → Good  
60–74 → Moderate  
Below 60 → Needs Improvement

---

## 6. Detected Issues or Violations

List any problems in the design.

For each issue include:

• Issue description  
• Technical impact  
• Vastu implication  
• Severity (Minor / Moderate / Major)

---

## 7. Design Improvement Recommendations

Provide practical suggestions to improve the layout.

Examples:

• Relocate a room  
• Adjust circulation  
• Improve ventilation  
• Adjust room proportions  
• Improve orientation  

Recommendations must be actionable.

---

## 8. Final Compliance Verdict

Provide a short professional conclusion summarizing:

• Overall Vastu compliance  
• KPBR compliance status  
• Suitability for construction planning  

End with a clear final status:

**COMPLIANT**  
**MINOR CHANGES REQUIRED**  
**REQUIRES MAJOR CORRECTIONS**

------------------------------------------------------------

Inputs:

User Requirements:
{requirements_json}

Generated Floor Plan Prompt:
{prompt_text}

Retrieved Vastu and KPBR Rules:
{constraints_text}

Important rules:

• Maintain professional architectural tone  
• Avoid excessive storytelling  
• Use clear structure and bullet lists  
• Avoid speculation if rules are unclear  
• Ensure the report reads like a professional architectural audit
"""

        chain = PromptTemplate(
            input_variables=["requirements_json", "prompt_text", "constraints_text", "current_date"],
            template=template,
        ) | llm

        print("Generating detailed Vastu/KPBR report in reference style...")
        response = chain.invoke(
            {
                "requirements_json": json.dumps(reqs, indent=2),
                "prompt_text": prompt_text,
                "constraints_text": constraints_text,
                "current_date": datetime.now().strftime("%Y-%m-%d"),
            }
        )

        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(response.content.strip())

        print(f"Report saved to {REPORT_FILE}")
        return True

    except Exception as e:
        print(f"Error generating report via Gemini: {e}")
        return False


if __name__ == "__main__":
    generate_vastu_report()
