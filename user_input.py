import os
import re
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
    reqs['bedrooms'] = input("Total Number of Bedrooms [Default: 3]: ") or "3"
    reqs['bathrooms'] = input("Number of Bathrooms [Default: 3]: ") or "3"
    reqs['kitchen'] = input("Kitchen (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['livingRoom'] = input("Living Room (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['diningArea'] = input("Dining Area (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['poojaRoom'] = input("Pooja Room (Yes/No) [Default: Yes]: ") or "Yes"
    reqs['studyRoom'] = input("Study Room / Home Office (Optional) [Default: No]: ") or "No"
    reqs['parking'] = input("Parking / Garage (Yes/No) [Default: Yes]: ") or "Yes"

    print("\n--- 3A. Ground Floor Bedroom Preference ---")
    reqs['preferGroundFloorBedrooms'] = input("Prefer bedrooms on Ground Floor? (Yes/No) [Default: No]: ") or "No"
    if str(reqs['preferGroundFloorBedrooms']).strip().lower() in {"yes", "y", "true", "1"}:
        reqs['groundFloorBedrooms'] = input("How many bedrooms on Ground Floor? [Default: 1]: ") or "1"
    else:
        reqs['groundFloorBedrooms'] = "1"

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


def _safe_num(v: str, fallback: float) -> float:
    m = re.search(r"[\d.]+", str(v))
    return float(m.group()) if m else fallback


def _yn(v: str) -> bool:
    return str(v).strip().lower() in {"yes", "y", "true", "1"}


def _build_cad_prompt(reqs: dict, rule_block: str) -> str:
    plot_w = _safe_num(reqs.get("plotWidth", "30"), 30.0)
    plot_l = _safe_num(reqs.get("plotLength", "40"), 40.0)
    floors = str(reqs.get("floors", "G+1")).strip()
    facing = str(reqs.get("facing", "East")).strip().capitalize()
    building_type = str(reqs.get("buildingType", "Independent house")).strip()
    bedrooms = int(_safe_num(reqs.get("bedrooms", "3"), 3))
    bathrooms = int(_safe_num(reqs.get("bathrooms", "3"), 3))
    builtup = reqs.get("builtUpArea", "1200")
    layout_pref = reqs.get("layoutPreferences", "Open Kitchen, Internal Stairs")
    output_format = reqs.get("outputFormat", "2D Floor Plan")
    prefer_gf = _yn(reqs.get("preferGroundFloorBedrooms", "No"))
    gf_bedrooms = int(_safe_num(reqs.get("groundFloorBedrooms", "0"), 0)) if prefer_gf else 0
    gf_bedrooms = max(0, min(gf_bedrooms, bedrooms))

    feature_list = []
    if _yn(reqs.get("kitchen", "Yes")):
        feature_list.append("Kitchen")
    if _yn(reqs.get("livingRoom", "Yes")):
        feature_list.append("Living Room")
    if _yn(reqs.get("diningArea", "Yes")):
        feature_list.append("Dining Area")
    if _yn(reqs.get("poojaRoom", "Yes")):
        feature_list.append("Pooja Room")
    if _yn(reqs.get("studyRoom", "No")):
        feature_list.append("Study Room")
    if _yn(reqs.get("parking", "Yes")):
        feature_list.append("Parking")

    gf_rule_text = (
        f"- Ground floor bedroom preference: YES. Place exactly {gf_bedrooms} bedroom(s) on Ground Floor.\n"
        if prefer_gf
        else "- Ground floor bedroom preference: NO specific count required.\n"
    )

    return (
        "Create an ultra realistic and highly attractive, fully rendered modern 2D CAD floor plan sheet (top view only).\n\n"
        "STYLE:\n"
        "- Pure white background outside plot, white inner floors with colored, realistic modern furniture.\n"
        "- Plot boundary filled with dense, realistic green grass and plants to clearly show setbacks. Car in driveway.\n\n"
        "COMPOSITION:\n"
        f"- Top center: '{facing.upper()}-FACING {building_type.upper()}' and '{int(plot_w)}ft x {int(plot_l)}ft PLOT'.\n"
        "- Ground Floor laid out left, First Floor alongside it.\n"
        "- Bottom Left: LEGEND (Walls/Doors/Windows).\n\n"
        "PROJECT SPECIFICS:\n"
        f"- Plot Dimensions: {plot_w}ft x {plot_l}ft plot. (You MUST annotate outer plot dimensions {plot_w}ft and {plot_l}ft with arrows!).\n"
        f"- Rooms: {', '.join(feature_list) if feature_list else 'Standard'}.\n"
        f"{gf_rule_text}\n"
        "LAYOUT & PLACEMENT RULES (CRITICAL):\n"
        "1. ALL ROOMS, ENTRANCES, AND STAIRCASE MUST BE PLACED EXACTLY AS DICTATED IN THE 'ROOM_PLACEMENTS' SECTION BELOW.\n"
        "2. Any deviation from the explicit 'ROOM_PLACEMENTS' mapping is a fatal failure.\n"
        f"3. Strict user layout preferences: {layout_pref.upper()}. If 'Internal Stairs' is specified, the stairs MUST be fully enclosed within the main exterior walls of the house, NOT external.\n"
        f"4. Parking MUST be placed in the front of the house, oriented towards the {facing} direction (facing the road).\n"
        "5. The Kitchen and Dining Area MUST be directly adjacent to each other.\n\n"
        "DETAILING & SETBACKS (CRITICAL):\n"
        "- Building MUST NOT touch the plot walls. It MUST be visibly centered with an explicit, visually distinct wide green setback track enclosing the entire house.\n"
        "- Ensure there is a highly visible, physically distinct gap between the outer boundary wall and the house's exterior walls.\n"
        "- STRICTLY label ALL 4 side clearances (Front, Rear, Left, Right) using 'SETBACK [value in m]' ON the green space.\n"
        "- ENTRANCE ANNOTATION: The Main Entrance MUST be explicitly annotated with a large text label 'MAIN ENTRANCE' and a directional arrow.\n"
        "- Wall thickness clearly shown. Doors have swing arcs. Windows have W1/W2 tags.\n"
        "- ROOM LABELS: Every single room MUST have a large text label inside it (e.g. LIVING ROOM, KITCHEN, BEDROOM) + room dimensions.\n"
        f"- PLOT LABELS: Overall {plot_w}ft x {plot_l}ft dimensions must be drawn with arrowheads on the outer compound wall.\n\n"
        "VASTU/KPBR RULES AND ROOM MAPPINGS:\n"
        f"{rule_block}\n\n"
        "DO NOT INCLUDE (FATAL ERRORS):\n"
        "- NO 3D/Isometric. NO door/window measurement boxes (e.g., DO NOT show D1=4x7).\n"
        "- NO blurry text. No unlabelled rooms.\n"
    )


def generate_prompt_from_dict(reqs: dict) -> str:
    """
    Uses RAG for Vastu/KPBR constraints and then composes a deterministic CAD-focused
    prompt to improve 2D floor plan image consistency.
    """
    print("\n==================================================")
    print("Generating Optimized Prompt using Vastu RAG Agent...")
    print("==================================================")

    qa_chain, _ = setup_rag(["vastu-for-home.pdf", "LSGD-KPBR-Amendment.pdf"])

    if not qa_chain:
        print("Failed to initialize Vastu RAG context.")
        return ""

    plot_w = _safe_num(reqs.get("plotWidth", "30"), 30.0)
    plot_l = _safe_num(reqs.get("plotLength", "40"), 40.0)
    floors = str(reqs.get("floors", "G+1")).strip()
    facing = str(reqs.get("facing", "East")).strip().capitalize()
    building_type = str(reqs.get("buildingType", "Independent house")).strip()
    bedrooms = int(_safe_num(reqs.get("bedrooms", "3"), 3))
    bathrooms = int(_safe_num(reqs.get("bathrooms", "3"), 3))
    vastu_level = reqs.get("vastuCompliance", "High")
    layout_pref = reqs.get("layoutPreferences", "Open Kitchen, Internal Stairs")
    style = reqs.get("style", "Modern")
    built_up = reqs.get("builtUpArea", "1200")
    print("\n--- 3A. Ground Floor Bedroom Preference ---")
    reqs['preferGroundFloorBedrooms'] = "Yes" # ALWAYS ensure at least 1 ground floor bedroom via prompt injection, regardless of original input.
    reqs['groundFloorBedrooms'] = reqs.get("groundFloorBedrooms", "1")
    if int(_safe_num(reqs['groundFloorBedrooms'], 0)) < 1:
        reqs['groundFloorBedrooms'] = "1"
    
    prefer_gf = "Yes" # Override prompt logic
    gf_bedrooms = int(_safe_num(reqs.get("groundFloorBedrooms", "1"), 1))

    feature_list = []
    if _yn(reqs.get("kitchen", "Yes")): feature_list.append("Kitchen")
    if _yn(reqs.get("livingRoom", "Yes")): feature_list.append("Living Room")
    if _yn(reqs.get("diningArea", "Yes")): feature_list.append("Dining Area")
    if _yn(reqs.get("poojaRoom", "Yes")): feature_list.append("Pooja Room")
    if _yn(reqs.get("studyRoom", "No")): feature_list.append("Study Room")
    if _yn(reqs.get("parking", "Yes")): feature_list.append("Parking")
    
    if floors.lower() not in {"ground", "g", "1", "single"}:
        feature_list.append("Balcony (First Floor)")

    rag_query = (
        "You are an Expert Architectural Planner and Vastu Master. Based on the project details, you must assign an explicit visual layout location "
        "and compass direction (e.g., Top-Right (Northeast), Bottom-Left (Southwest), Center) to EVERY single room requested, according to strict Vastu principles.\n\n"
        "Return ONLY the following section. Do not output ANY other abstract rules or hints:\n"
        "1) ROOM_PLACEMENTS (CRITICAL: You MUST break this down explicitly into '*Ground Floor Plan*' and '*First Floor Plan*' (if G+1 or more). "
        "For EACH floor, list EVERY room, its exact visual location (Top/Bottom/Left/Right/Center) AND direction, and provide *Deep Architectural & Vastu Reasoning*. "
        "The reasoning MUST be highly detailed (2-3 sentences per room), explaining the energetic benefits, airflow, sunlight, and exact Vastu Shastra principles applied. "
        f"Example format: '*Main Entrance*: Center-Right (East). Opens into Living Room. *Reasoning: Placing the entrance in the Eastern Pada invokes positive solar energy (Indra) and ensures the morning sunlight penetrates deep into the living spaces, promoting health and vitality. This aligns perfectly with the {facing}-facing plot dynamics.'\n"
        "The Main Entrance MUST explicitly state it opens directly into the Living Room (or Lobby). "
        "The Parking MUST be placed in the {facing} direction (front of the house). "
        "The Kitchen MUST be placed adjacent to the Dining Area. "
        "If a Pooja Room is included in the requirements, it MUST be placed on the Ground Floor plan for accessibility and grounding. "
        "CRITICAL: Every single room placement (not just Pooja) MUST have a detailed, logical architectural and Vastu-based reasoning that dictates its specific location. "
        "Ensure every requested room, bathroom, entrance, and stair is placed.)\n\n"
        f"Project details: {plot_w} ft x {plot_l} ft, {facing}-facing plot, {floors}, "
        f"{bedrooms} bedrooms ({gf_bedrooms} on GF MUST BE INCLUDED), {bathrooms} bathrooms, building type: {building_type}.\n"
        f"MUST ASSIGN LOCATIONS FOR: Main Entrance, Stairs, {', '.join(feature_list) if feature_list else 'Standard rooms'}, {bedrooms} Bedrooms, {bathrooms} Bathrooms.\n"
        f"Layout preferences: {layout_pref}, architectural style: {style}, "
        f"vastu compliance preference: {vastu_level}. "
        "Keep response comprehensive but strictly focused on the requested formats."
    )

    try:
        rag_result = qa_chain.invoke({"input": rag_query})
        rule_block = rag_result["answer"].strip()
        optimized_prompt = _build_cad_prompt(reqs, rule_block)

        print("============================================================")
        print("\n=== OPTIMIZED PROMPT FOR 2D FLOOR PLAN AI ===")
        print("============================================================")
        print("Here is the highly optimized and detailed prompt for an AI image generator:\n")
        print(optimized_prompt)
        print("\n=============================================")

        with open("optimized_prompt_output.txt", "w", encoding="utf-8") as f:
            f.write(optimized_prompt)

        return optimized_prompt
    except Exception as e:
        print(f"Error generation prompt from RAG: {e}")
        return ""


if __name__ == "__main__":
    reqs = get_user_input()
    generate_prompt_from_dict(reqs)
