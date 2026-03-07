import os
from rag_vastu import setup_rag

def get_user_input():
    print("============================================================")
    print(" Vastu AI - Floor Plan Input Collection Module")
    print("============================================================")
    
    reqs = {}
    
    print("\n--- 1. Plot & Site Details ---")
    reqs['plotLength'] = input("Plot Length (ft/m) [Default: 40 ft]: ") or "40"
    reqs['plotWidth'] = input("Plot Width (ft/m) [Default: 30 ft]: ") or "30"
    reqs['plotShape'] = input("Plot Shape (Square/Rectangle/Irregular) [Default: Rectangle]: ") or "Rectangle"
    reqs['facing'] = input("Plot Facing Direction (North/East/South/West) [Default: East]: ") or "East"
    
    print("\n--- 2. Building Configuration ---")
    reqs['floors'] = input("Number of Floors (Ground, G+1, G+2, etc.) [Default: G+1]: ") or "G+1"
    reqs['builtUpArea'] = input("Total Built-up Area (optional) [Default: 1200 sqft]: ") or "1200"
    reqs['buildingType'] = input("Type of Building (Independent house/Villa/Duplex) [Default: Independent house]: ") or "Independent house"
    
    print("\n--- 3. Room Requirements ---")
    reqs['bedrooms'] = input("Number of Bedrooms [Default: 3]: ") or "3"
    reqs['bathrooms'] = input("Number of Bathrooms [Default: 3]: ") or "3"
    reqs['kitchen'] = input("Kitchen (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['livingRoom'] = input("Living Room (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['diningArea'] = input("Dining Area (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['poojaRoom'] = input("Pooja Room (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['studyRoom'] = input("Study Room / Home Office (Optional) [Default: No]: ") or "No"
    reqs['parking'] = input("Parking / Garage (Yes/No) [Default: Yes]: ") or "Yes"
    
    print("\n--- 4. Vastu Compliance Preference ---")
    print("Levels: Low, Medium, High")
    reqs['vastuCompliance'] = input("Vastu Compliance Level [Default: High]: ") or "High"
    
    print("\n--- 5. Room & Layout Preferences (Optional) ---")
    reqs['layoutPreferences'] = input("Any specific layout preferences? (e.g., Open kitchen, stairs inside) [Default: Open Kitchen, Internal Stairs]: ") or "Open Kitchen, Internal Stairs"
    
    print("\n--- 6. Design & Style Preferences ---")
    reqs['style'] = input("Architectural Style (Modern/Traditional/Minimal) [Default: Modern]: ") or "Modern"
    
    print("\n--- 7. Output & Export Options ---")
    reqs['outputFormat'] = input("Output Format (2D Floor Plan / 3D View) [Default: 2D Floor Plan]: ") or "2D Floor Plan"
    
    return reqs

def generate_prompt_from_dict(reqs: dict) -> str:
    """
    Takes a dictionary of user requirements,
    constructs an architecture plan context, invokes the Vastu/KPBR RAG system,
    and returns a highly structured optimized prompt for DALL-E 3 image generation.
    """
    print("\n==================================================")
    print("Generating Optimized Prompt using Vastu RAG Agent...")
    print("==================================================")
    
    qa_chain, _ = setup_rag(["vastu-for-home.pdf", "LSGD-KPBR-Amendment.pdf"])
    
    if not qa_chain:
        print("Failed to initialize Vastu RAG context.")
        return ""

    facing_val = reqs.get('facing').capitalize()
    direction_map = {
        "North": "TOP",
        "South": "BOTTOM",
        "East": "RIGHT",
        "West": "LEFT"
    }
    context_prompt = (
        f"A hyper-realistic, professional, high-definition 2D architectural CAD floor plan on a clean white background, "
        f"depicting a {reqs.get('style').lower()}, Vastu-compliant {reqs.get('floors')} {reqs.get('buildingType').lower()} "
        f"on an {reqs.get('facing')}-facing {reqs.get('plotShape').lower()} plot measuring {reqs.get('plotWidth')}' (Width) x {reqs.get('plotLength')}' (Depth). "
        f"The design emphasizes {reqs.get('style').lower()} aesthetics while strictly following Vastu principles for room placements.\n\n"
        
        f"*Ground Floor Plan (Plot Dimensions: {reqs.get('plotWidth')}' x {reqs.get('plotLength')}')*:\n"
        f"The ground floor layout prioritizes Vastu placements for {reqs.get('facing')}-facing plots.\n"
        f"For each requested room: Kitchen, Living Room, Dining Area, Pooja Room, Study Room, and requested bedrooms/bathrooms, output exactly like this:\n"
        f"*   *[Room Name]*: [Location description]. *Reasoning: [Explanation based on Vastu context].\n"
        f"*   *Internal Stairs*: An internal staircase is included for circulation to the first floor. Positioned for efficient access without infringing upon critical Vastu zones.\n"
        f"*   *Parking Area*: A designated parking space is provided within the plot boundaries. Located at the front or side, respecting necessary setbacks.\n"
        f"*   *KPBR Setbacks*: Calculate and strictly provide the Front, Rear, and Side minimum setback open spaces required from the KPBR context for this plot size.\n\n"
        
        f"*First Floor Plan*:\n"
        f"For each requested upper-floor room (Master Bedroom, extra bedrooms, etc.), output exactly like this:\n"
        f"*   *[Room Name]*: [Location description]. *Reasoning: [Explanation based on Vastu context].\n"
        f"*   *Balcony*: A spacious balcony extending from the East or North side of the first floor, enhancing natural light and views.\n\n"
        
        f"*Visuals & Architectural Components*:\n"
        f"The generated 2D floor plan image MUST include the following professional architectural drawing components:\n"
        f"*   **CRITICAL MULTI-FLOOR RULE**: If multiple floors are requested (e.g., Ground & First Floor), they MUST be drawn side-by-side on the SAME single image canvas (Ground Floor strictly on the LEFT, First Floor strictly on the RIGHT).\n"
        f"*   Clear, legible English text labels for every single room, area, and exterior boundary, rendered without any spelling errors.\n"
        f"*   Accurate, consistent numerical measurements displayed along the walls for every individual room (e.g., 12'-0\" x 10'-0\", 3.65m x 3.05m).\n"
        f"*   Prominent door swings clearly indicating the open direction for every door.\n"
        f"*   Clear window markings on all exterior walls.\n"
        f"*   Structural pillars (where architecturally appropriate).\n"
        f"*   Distinctly shaded walls to differentiate them from open spaces.\n"
        f"*   A clear compass/cardinal direction indicator (North arrow, East, South, West labels) prominently placed in the corner of the image, unequivocally showing the {reqs.get('facing')}-facing orientation of the plot and house.\n"
        f"*   The overall built-up area of {reqs.get('builtUpArea')} sqft (spread over {reqs.get('floors')} floors) should be clearly indicated.\n"
        f"*   The KPBR setbacks MUST be physically written in the open exterior space around the house.\n"
        f"*   All spatial arrangements and room placements must perfectly match the Vastu-compliant definitions provided above.\n"
    )

    try:
        result = qa_chain.invoke({"input": context_prompt})
        optimized_prompt = result["answer"].strip()
        print("============================================================")
        print("\n=== OPTIMIZED PROMPT FOR 2D FLOOR PLAN AI ===")
        print("============================================================")
        print("Here is the highly optimized and detailed prompt for an AI image generator, precisely adhering to your Vastu requirements and critical instructions:\n")
        print(optimized_prompt)
        print("\n=============================================")
        
        # Write to disk for legacy file-system passing
        with open("optimized_prompt_output.txt", "w", encoding="utf-8") as f:
            f.write(optimized_prompt)
            
        return optimized_prompt
    except Exception as e:
        print(f"Error generation prompt from RAG: {e}")
        return ""

if __name__ == "__main__":
    reqs = get_user_input()
    generate_prompt_from_dict(reqs)
