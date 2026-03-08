import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

def generate_vastu_report():
    """
    Reads the generated prompt requirements and uses Gemini to craft a 
    beautifully formatted 8-section Markdown Vastu Compliance Report.
    """
    prompt_file = "optimized_prompt_output.txt"
    if not os.path.exists(prompt_file):
        print(f"Error: {prompt_file} not found.")
        return False
        
    with open(prompt_file, 'r', encoding='utf-8') as f:
        plan_details = f.read()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return False

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
        template = """
        You are a Master Vastu Shastra Consultant and Expert Architect.
        Based on the following 2D floor plan generation prompt that was just executed, 
        create a highly professional, exactly 8-section Markdown compliance report.
        
        Plan Details:
        {plan_details}
        
        Your report MUST exactly follow this 8-section structure using these exact headers and emojis:
        
        ## 1️⃣ Project Overview & User Inputs
        (Use a clean Markdown table to list ALL raw architectural inputs provided by the user.
        Include rows for: Plot Dimensions, Facing Direction, Total Floors, Building Type, Total Bedrooms requested, Ground Floor Preferences, and Room Layout constraints.)
        
        ## 2️⃣ Floor Plan Layout Summary
        (A clear, professional architectural paragraph explaining the spatial organization and layout flow.)
        
        ## 3️⃣ Vastu Compliance Analysis
        (Provide a detailed evaluation of room placements using a Markdown table. 
        Columns exactly as follows: | Space/Room | Placed Direction | Vastu Rule/Principle | Status |
        For Status, use bold evaluative text like **Excellent**, **Good**, or **Non-Compliant**.)
        
        ## 4️⃣ Constraints & Dimensional Rules
        (Evaluate adherence to local regulation constraints and explicit user overrides. Detail setbacks, building rules, or special user requests (like 'Parking in front'). Use bullet points or a table.)
          
        ## 5️⃣ Vastu / Compliance Score
        (Prominently display a numerical score out of 100. Provide a short, structured breakdown of how the points were awarded.)
        
        ## 6️⃣ Detected Issues & Violations
        (Numbered list if any rules are broken. Provide clear impact statements. If none, write "No major issues detected. Layout is highly compliant.")
        
        ## 7️⃣ Actionable Recommendations
        (Numbered list of highly professional architectural and Vastu suggestions to optimize the layout further.)
        
        ## 8️⃣ Final Compliance Status
        (A striking final conclusion statement in bold, e.g., **MINOR CHANGES RECOMMENDED** or **FULLY COMPLIANT MASTER PLAN**)
        
        Format beautifully with modern markdown tables, bold text, bulleted lists, and headers. Ensure the tone is extremely professional, authoritative, and structured like a high-end architectural consultant report. Do not include introductory or concluding conversational filler.
        """
        
        prompt = PromptTemplate(input_variables=["plan_details"], template=template)
        chain = prompt | llm
        
        print("\nGenerating comprehensive Vastu Report...")
        response = chain.invoke({"plan_details": plan_details})
        
        with open('vastu_compliance_report.md', 'w', encoding='utf-8') as f:
            f.write(response.content)
            
        print("Report saved successfully to vastu_compliance_report.md")
        return True
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

if __name__ == "__main__":
    generate_vastu_report()
