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
        create a highly professional, exactly 8-section Markdown compliance report.
        
        Plan Details:
        {plan_details}
        
        Your report MUST exactly follow this 8-section structure using these exact headers and emojis:
        
        ## 1️⃣ Project Overview
        (Basic details, dimensions, facing in bullet points)
        
        ## 2️⃣ Generated Floor Plan Summary
        (Short paragraph layout explanation, room positions)
        
        ## 3️⃣ Vastu Compliance Analysis
        (Detailed evaluation of room placements. MUST bold the evaluation word, e.g., "**Main Entrance (North): Excellent.**" or "**Good.**" or "**Mixed.**")
        
        ## 4️⃣ KPBR / Building Rule Compliance
        (Local regulation constraints check. For setbacks, use a sub-bullet list formatting like:
        * Setbacks:
          * Front Setback (North): 3 meters - **Compliant.**
          * Rear Setback (South): 1 meter - **Compliant.**)
          
        ## 5️⃣ Vastu Score / Compliance Score
        (Numerical score out of 100 with a breakdown of points)
        
        ## 6️⃣ Detected Issues / Violations
        (Numbered list if any rules are broken. If none, write "None.")
        
        ## 7️⃣ Recommendations
        (Numbered list of suggestions to improve)
        
        ## 8️⃣ Final Compliance Status
        (A single bold phrase: e.g., **MINOR CHANGES NEEDED.** or **FULLY COMPLIANT.**)
        
        Format beautifully with bolding, lists, and markdown headers. No introduction or conclusion paragraphs outside these 8 sections.
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
