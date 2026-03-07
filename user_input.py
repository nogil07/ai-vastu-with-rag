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
    canvas_side = direction_map.get(facing_val, "BOTTOM")

    context_prompt = (
        f"You are generating a blueprint based on these explicit parameters:\n"
        f"- Plot: {reqs.get('plotWidth')}x{reqs.get('plotLength')} ({reqs.get('plotShape')}, {reqs.get('builtUpArea')} sqft).\n"
        f"- Target Rooms: {reqs.get('bedrooms')} Beds, {reqs.get('bathrooms')} Baths, Kitchen ({reqs.get('kitchen')}), Living ({reqs.get('livingRoom')}), Dining ({reqs.get('diningArea')}), Pooja ({reqs.get('poojaRoom')}), Study ({reqs.get('studyRoom')}), Parking ({reqs.get('parking')}).\n"
        f"- Vastu Level: {reqs.get('vastuCompliance')}\n\n"
        
        f"Output MUST be structured EXACTLY like this optimized format:\n\n"
        
        f"A hyper-realistic, professional, high-definition 2D architectural CAD floor plan...\n\n"
        
        f"*** [0. CRITICAL ANTI-HALLUCINATION RULES] ***\n"
        f"1. DO NOT invent or draw any rooms/features not explicitly requested above.\n"
        f"2. Use clean, perfect English for ALL text labels. No misspellings.\n"
        f"3. Maximize interior space utilization. Do not leave vast empty indoor zones.\n\n"
        
        f"*** [1. PLOT ORIENTATION & SETBACKS] ***\n"
        f"- **Compass**: Top Right Corner. Compass MUST point NORTH towards the TOP of the image explicitly.\n"
        f"- **Canvas Alignment**: Because this is an {facing_val}-facing plot, the main road, the physical entrance gate, and the car parking MUST be drawn explicitly on the {canvas_side} side of the image canvas. \n"
        f"- **KPBR Setbacks**: Visually enforce Kerala Building Rules. Depict the main house structure strictly recessed from the plot boundary walls using green lawns or driveway space. You MUST explicitly draw these mathematical setback distances (e.g., '3.0m', '1.5m') physically inside these open boundary spaces on all 4 sides.\n\n"
        
        f"*** [2. ROOM LAYOUT & DIMENSIONS] ***\n"
        f"*Ground Floor Plan (LEFT HALF OF CANVAS)*:\n"
        f"Calculate Vastu placements, but DO NOT output your reasoning. For each explicitly requested ground floor room, output ONLY its exact physical location, furniture layout, and the required text callout:\n"
        f"- [Room Name]: [Physical location, e.g., 'Located in the Northeast corner']. [Furniture/details]. The text '[ROOM NAME] [Calculated Dimension]' is explicitly drawn inside the room.\n"
        f"...\n\n"
        
        f"*First Floor Plan (RIGHT HALF OF CANVAS)*:\n"
        f"For each explicitly requested first floor room, output ONLY its physical location, furniture layout, and required text callout:\n"
        f"- [Room Name]: [Physical location]. [Furniture/details]. The text '[ROOM NAME] [Calculated Dimension]' is explicitly drawn inside the room.\n"
        f"...\n\n"
        
        f"*** [3. VISUAL STYLE & TYPOGRAPHY] ***\n"
        f"- **Layout Design**: A premium, magazine-quality architectural presentation board infographic. Ground Floor Plan on the LEFT, First Floor Plan on the RIGHT, side-by-side.\n"
        f"- **Header Banner**: A sleek, modern title: '{facing_val.upper()}-FACING INDEPENDENT HOUSE' with elegant sub-text '{reqs.get('plotWidth')}\" x {reqs.get('plotLength')}\" PLOT ({reqs.get('floors')})'.\n"
        f"- **Legends (DRAW EXACTLY ONE)**: In the Bottom Left Corner, draw exactly ONE unified 'LEGEND' box explaining symbols for Wall, Door, Window, Stairs. In the Bottom Right Corner, draw ONE 'VASTU COMPLIANCE' summary box.\n"
        f"- **CAD Styling**: Ultra-high definition photorealistic textures, lush green landscaping outside the plot, modern wooden furniture staging inside, clear outer boundary walls.\n"
        f"- **Dimensional Typography**: Below EVERY room name, explicitly render the exact metrics (e.g. '15\" x 18\"') in bold, readable, crisp text.\n"
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
