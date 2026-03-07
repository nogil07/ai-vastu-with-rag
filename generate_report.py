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
        You are a Master Vastu Shastra Consultant and Architect.
        Based on the following 2D floor plan generation prompt that was just executed, 
        create a highly professional, 8-section Markdown compliance report.
        
        Plan Details:
        {plan_details}
        
        Your report MUST exactly follow this 8-section structure:
        1. Project Overview (Basic details, dimensions, facing)
        2. Generated Floor Plan Summary (Layout explanation, room positions)
        3. Vastu Compliance Analysis (Detailed evaluation of room placements)
        4. KPBR / Building Rule Compliance (Local regulation constraints check)
        5. Vastu Score / Compliance Score (Numerical score out of 100)
        6. Detected Issues / Violations (If any rules are broken)
        7. Recommendations (Suggestions to improve)
        8. Final Compliance Status (Pass/Fail/Pass with conditions)
        
        Format beautifully with bolding, lists, and markdown headers (##).
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
