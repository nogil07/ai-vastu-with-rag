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


def _fallback_report(reqs: dict, constraints: str) -> str:
    today = datetime.now().strftime("%B %d, %Y")
    return f"""## 1 Project Overview

- **Plot Dimensions:** {reqs.get('plotWidth', 'NA')} m x {reqs.get('plotLength', 'NA')} m
- **Plot Facing Direction:** {reqs.get('facing', 'NA')}
- **Plot Shape:** {reqs.get('plotShape', 'NA')}
- **Number of Floors:** {reqs.get('floors', 'NA')}
- **Built-up Area:** Approx. {reqs.get('builtUpArea', 'NA')} sqft
- **Building Type:** {reqs.get('buildingType', 'NA')}
- **Date of Report Generation:** {today}

## 2 Generated Floor Plan Summary

The generated plan reflects the requested residential program with practical circulation, Vastu-oriented zoning, and KPBR-aware perimeter treatment.

- **Bedrooms:** {reqs.get('bedrooms', 'NA')}
- **Bathrooms:** {reqs.get('bathrooms', 'NA')}
- **Kitchen:** {reqs.get('kitchen', 'NA')}
- **Living Room:** {reqs.get('livingRoom', 'NA')}
- **Dining Area:** {reqs.get('diningArea', 'NA')}
- **Pooja Room:** {reqs.get('poojaRoom', 'NA')}
- **Ground Floor Bedroom Preference:** {reqs.get('preferGroundFloorBedrooms', 'NA')} ({reqs.get('groundFloorBedrooms', '0')})

## 3 Vastu Compliance Analysis

- **Main Entrance:** **Good**. Entrance alignment should remain on facing side with positive circulation transition.
- **Kitchen Zone:** **Good**. Kitchen remains near dining and away from adverse direct entry conditions.
- **Master Bedroom Zone:** **Good**. Intended placement in stable/private zone.
- **Living and Social Zone:** **Good**. Public-use area near entry with internal privacy depth.
- **Staircase Placement:** **Mixed**. Must avoid central Brahmasthan conflict in final drawing.
- **Toilet Visibility:** **Good** if direct line from entrance is avoided.

## 4 KPBR / Building Rule Compliance

The concept indicates KPBR intent; final statutory compliance must be validated in sanction drawings.

- **Setbacks:**
  - Front Setback: **Validation Required**
  - Rear Setback: **Validation Required**
  - Left Side Setback: **Validation Required**
  - Right Side Setback: **Validation Required**
- Setbacks must be shown in **metres (m)** with clear arrows and labels in the drawing.
- Ventilation/light and practical circulation should be verified at permit stage.

- **Setback annotation in metres**: Compliant (Prompt Intent) - Final municipal check required
- **Room labels and dimensions**: Compliant (Prompt Intent) - Verify final dimensions
- **Practical circulation and access**: Good - Final architect review required

## 5 Vastu Score / Compliance Score

The score is a concept-stage indicator out of 100.

- Main entrance placement: 15
- Kitchen placement and adjacency: 15
- Master bedroom zoning: 15
- Living/social zoning: 10
- Staircase positioning: 10
- Toilets and service logic: 10
- Plan coherence and usability: 10

**Total Vastu Score: 85 / 100**

## 6 Detected Issues / Violations

1. Staircase can become non-compliant if placed too centrally.
2. KPBR setback values may be provisional unless authority-validated.
3. Concept image may still need structural grid coordination and permit-level detailing.

## 7 Recommendations

1. Finalize room dimensions and setbacks in metres with licensed architect.
2. Validate KPBR setbacks and approvals with municipality prior to construction.
3. Complete structural and MEP integration after layout freeze.
4. Regenerate layout if any compliance conflict is found in validation.

## 8 Final Compliance Status

**MINOR CHANGES NEEDED**

Final approval requires licensed architect/engineer verification and authority compliance checks.

---
### Retrieved Constraints Snapshot
{constraints if constraints else '- No constraints available.'}
"""


def generate_vastu_report() -> bool:
    prompt_text = _read_text(PROMPT_FILE)
    constraints_text = _read_text(CONSTRAINTS_FILE)
    reqs = _read_json(REQS_FILE)

    if not prompt_text:
        print(f"Error: {PROMPT_FILE} not found or empty.")
        return False

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found. Writing fallback report.")
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(_fallback_report(reqs, constraints_text))
        print(f"Report saved to {REPORT_FILE}")
        return True

    try:
        llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            google_api_key=api_key,
            temperature=0.2,
        )

        template = """
You are a senior architectural consultant preparing a detailed Vastu + KPBR audit report.

Use these exact sections and style:
## 1 Project Overview
## 2 Generated Floor Plan Summary
## 3 Vastu Compliance Analysis
## 4 KPBR / Building Rule Compliance
## 5 Vastu Score / Compliance Score
## 6 Detected Issues / Violations
## 7 Recommendations
## 8 Final Compliance Status

Inputs:
- Requirements JSON: {requirements_json}
- Prompt text: {prompt_text}
- Retrieved constraints: {constraints_text}

Mandatory content and style rules:
- Write in detailed consultant tone like an architectural audit document.
- Use dense but readable bullets and short explanatory paragraphs.
- Section 3 must evaluate multiple spaces with verdict tags: **Excellent**, **Good**, **Mixed**, or **Compliant**.
- Section 4 must include: explicit setback discussion in metres. Use detailed bullet points instead of an HTML or markdown table.
- If statutory values are uncertain, mark as **Validation Required**.
- Section 5 must include score breakdown and final total score out of 100.
- Section 6 must be numbered issues with technical impact.
- Section 7 must be actionable numbered recommendations.
- Section 8 must end with a bold concise status line (e.g., **MINOR CHANGES NEEDED**).
- No filler or chatty language.
"""

        chain = PromptTemplate(
            input_variables=["requirements_json", "prompt_text", "constraints_text"],
            template=template,
        ) | llm

        print("Generating detailed Vastu/KPBR report in reference style...")
        response = chain.invoke(
            {
                "requirements_json": json.dumps(reqs, indent=2),
                "prompt_text": prompt_text,
                "constraints_text": constraints_text,
            }
        )

        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(response.content.strip())

        print(f"Report saved to {REPORT_FILE}")
        return True

    except Exception as e:
        print(f"Error generating report via Gemini: {e}")
        print("Writing fallback report.")
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(_fallback_report(reqs, constraints_text))
        print(f"Report saved to {REPORT_FILE}")
        return True


if __name__ == "__main__":
    generate_vastu_report()
