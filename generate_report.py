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
You are a master architectural consultant and Vastu Shastra expert preparing an exhaustive, premium Vastu and KPBR audit report. 
Your goal is to provide a highly detailed, professional, and profound analysis that exceeds standard expectations. DONT JUST LIST ITEMS, PROVIDE DEEP INSIGHTS.

Use these exact sections and style:
## 1 ❐ Project Overview
## 2 ❐ Generated Floor Plan Summary
## 3 ❐ Vastu Compliance Analysis
## 4 ❐ KPBR / Building Rule Compliance
## 5 ❐ Vastu Score / Compliance Score
## 6 ❐ Detected Issues / Violations
## 7 ❐ Recommendations
## 8 ❐ Final Compliance Status

Inputs:
- Requirements JSON: {requirements_json}
- Prompt text (contains explicit Vastu reasoning for layout): {prompt_text}
- Retrieved constraints (KPBR rules): {constraints_text}

Mandatory content and style rules:
- Tone: Highly authoritative, sophisticated, and deeply technical architectural consultant.
- Detail level: EXTREME. Write extensive, multi-sentence paragraphs for every point. Explain *why* a placement works, its impact on the home's energy (prana), natural light, ventilation, and circulation.
- Section 2: Detail the spatial flow. How does one move from the entrance to the private zones? Discuss the volume, connectivity, and functional ergonomics.
- Section 3: Evaluate EVERY single room mentioned in the Prompt Text. Provide profound Vastu insights referencing specific elements (Agni, Jal, Vayu, Prithvi, Akash) and directions (Eesanya, Agneya, Nairutya, Vayavya). Use verdict tags: **Excellent**, **Good**, **Mixed**, or **Non-Compliant**.
- Section 4: Explicit setback discussion in metres. Detail the implications of the structural footprint on the plot. Use comprehensive bullet points (NO TABLES). If statutory values are uncertain, mark as **Validation Required** but provide the estimated requirement.
- Section 5: Include a detailed score breakdown for at least 8 specific criteria, culminating in a final total score out of 100 with a descriptive rating (e.g., "Outstanding", "Needs Improvement").
- Section 6: Detail any compromises heavily. Explain the technical and energetic impact of each issue.
- Section 7: Provide highly actionable, precise recommendations for fixing issues or further elevating the spatial energy.
- Section 8: A powerful, commanding concluding paragraph followed by a bold concise status line (e.g., **MINOR CHANGES NEEDED**).
- Premium Delineation: Wrap key architectural insights or Vastu rationale in markdown blockquotes (`>`) to make them stand out. Use horizontal rules (`---`) between major sections to enhance visual clarity.
- Format: Use rich markdown formatting (bolding, italics, nested lists) to make the dense information highly readable and engaging.
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
        return False


if __name__ == "__main__":
    generate_vastu_report()
