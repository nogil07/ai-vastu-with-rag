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

    context_prompt = (
        f"Design an Architectural Floor Plan with the following criteria:\n"
        f"- Plot Dimensions: {reqs.get('plotWidth')}x{reqs.get('plotLength')}\n"
        f"- Plot Shape: {reqs.get('plotShape')}\n"
        f"- Plot Facing Direction: {reqs.get('facing')}\n"
        f"- Number of Floors: {reqs.get('floors')}\n"
        f"- Building Type: {reqs.get('buildingType')}\n"
        f"- Built-up Area: {reqs.get('builtUpArea')} sqft\n"
        f"- Layout Details: {reqs.get('bedrooms')} Bedrooms, {reqs.get('bathrooms')} Bathrooms\n"
        f"- Primary Rooms: Kitchen ({reqs.get('kitchen')}), Living Room ({reqs.get('livingRoom')}), Dining Area ({reqs.get('diningArea')}), Pooja Room ({reqs.get('poojaRoom')})\n"
        f"- Secondary Rooms: Study/Office ({reqs.get('studyRoom')}), Car Parking ({reqs.get('parking')})\n"
        f"CRITICAL RULES: DO NOT INCLUDE ANY ROOMS THAT ARE NOT EXPLICITLY REQUESTED ABOVE. Maximize space utilization for the requested rooms only.\n"
        f"- Parking Rule: If Parking is requested, it MUST be positioned strictly at the FRONT or SIDE of the house, fully within the plot boundary.\n"
        f"- Vastu Compliance Level Required: {reqs.get('vastuCompliance')}\n"
        f"- User Layout Preferences: {reqs.get('layoutPreferences')}\n"
        f"- Architectural Style Theme: {reqs.get('style')}\n\n"
        f"Using strict Vastu Shastra principles and KPBR constraints from your context, "
        f"derive the precise optimal positioning of each room.\n"
        f"Output MUST be structured EXACTLY like the following example format:\n\n"
        f"A hyper-realistic, professional, high-definition 2D architectural CAD floor plan...\n\n"
        f"*Ground Floor Plan (Plot Dimensions: ...)*:\n"
        f"The ground floor layout prioritizes...\n"
        f"*   *Main Entrance*: [Description and Reasoning]\n"
        f"*   *Living Room*: [Description and Reasoning]\n"
        f"...\n\n"
        f"*First Floor Plan*:\n"
        f"...\n\n"
        f"*KPBR Setback & Building Rule Constraints*:\n"
        f"Apply strict KPBR (Kerala Municipality Building Rules) to the {reqs.get('plotWidth')}x{reqs.get('plotLength')} plot. Visually enforce the following open spaces:\n"
        f"- *Front Setback*: [Calculate required minimum front open space from KPBR context based on plot size and road type].\n"
        f"- *Rear Setback*: [Calculate required minimum rear open space from KPBR context].\n"
        f"- *Side Setbacks*: [Calculate required minimum side open spaces from KPBR context].\n"
        f"- CRITICAL VISUAL REQUIREMENT: These exact setback dimensions MUST be drawn to scale in the floor plan. Show the main house structure explicitly recessed from the plot boundary walls, depicting the setbacks as green lawns, driveways, or paved open space surrounding the main building on all 4 sides.\n\n"
        f"*Visuals & Architectural Components (MANDATORY PRESENTATION BOARD STYLE)*:\n"
        f"The generated {reqs.get('outputFormat')} image MUST be designed as a professional architectural presentation board infographic, EXACTLY following this visual layout:\n"
        f"- **Layout**: A wide landscape canvas featuring the Ground Floor Plan on the LEFT half, and the First Floor Plan on the RIGHT half side-by-side.\n"
        f"- **Top Header Banner**: A bold, centered title reading '{reqs.get('facing').upper()}-FACING INDEPENDENT HOUSE' with a sub-banner '{reqs.get('plotWidth')}\" x {reqs.get('plotLength')}\" PLOT ({reqs.get('floors')})' underneath.\n"
        f"- **Top Right Corner**: A traditional compass rose (North arrow) with N, S, E, W labels.\n"
        f"- **Bottom Left Corner**: A visual 'LEGEND:' box explaining symbols for Wall, Door, Window, Stairs, Pillar, and Main Entrance (with corresponding visual icons).\n"
        f"- **Bottom Right Corner**: A green-bordered 'VASTU COMPLIANCE' summary box listing the strategic placements (e.g. Entrance: East, Pooja: NE).\n"
        f"- **Drawing Style**: High-definition, textured 2D CAD style with green landscaping (grass/plants) outside the plot, realistic car in the parking, and wooden furniture inside the rooms.\n"
        f"- **Typography**: Clearly legible room names (e.g. 'LIVING ROOM') with exact numerical dimensions below them (e.g. '15\" x 18\"').\n"
        f"- **Labels**: Clearly map out NORTH, SOUTH, EAST, WEST around the border of the ground plan.\n"
        f"Output nothing but the optimized visual prompt itself."
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
