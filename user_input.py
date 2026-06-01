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

def detect_total_floors(floor_text: str) -> int:
    floor_text = str(floor_text).strip().lower()

    if floor_text in {"ground", "g", "single", "1"}:
        return 1

    match = re.search(r"g\s*\+\s*(\d+)", floor_text)

    if match:
        return int(match.group(1)) + 1

    if "duplex" in floor_text:
        return 2

    if "triplex" in floor_text:
        return 3

    return 2

def get_floor_names(total_floors):
    names = [
        "GROUND FLOOR",
        "FIRST FLOOR",
        "SECOND FLOOR",
        "THIRD FLOOR",
        "FOURTH FLOOR"
    ]

    return names[:total_floors]


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

    total_floors = detect_total_floors(floors)
    floor_names = get_floor_names(total_floors)
    floor_layout_instruction = ""

    for floor in floor_names:
        floor_layout_instruction += f"- {floor} clearly separated and labeled.\n"
    composition_text = (
        "- Multi-floor plans arranged side-by-side horizontally.\n"
        if total_floors > 1
        else "- Single floor plan centered.\n"
    )


    return (
        "Create an ultra realistic 4k(cartoon styled) modern 2D CAD floor plan sheet.\n\n"
        "TOP VIEW ONLY.\n"
        "NO 3D.\n"
        "NO ISOMETRIC VIEW.\n\n"
        "STYLE:\n"
        "- Pure white background outside plot, white inner floors with colored, realistic modern furniture.\n"
        "- Plot boundary filled with dense, realistic green grass and plants to clearly show setbacks. Car in driveway.\n\n"



        "FLOOR DISPLAY:\n"
        f"{floor_layout_instruction}\n"

        "COMPOSITION:\n"
        f"- Top center: '{facing.upper()}-FACING {building_type.upper()}' and '{int(plot_w)}ft x {int(plot_l)}ft PLOT'.\n"
        f"{composition_text}"
        "- Bottom Left: LEGEND (Walls/Doors/Windows).\n\n"
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
        
        "- NO blurry text. No unlabelled rooms.\n"
    )


_QA_CHAIN = None

def get_qa_chain():
    global _QA_CHAIN
    if _QA_CHAIN is None:
        _QA_CHAIN, _ = setup_rag(["vastu-for-home.pdf", "LSGD-KPBR-Amendment.pdf"])
    return _QA_CHAIN

def generate_prompt_from_dict(reqs: dict) -> str:
    """
    Uses RAG for Vastu/KPBR constraints and then composes a deterministic CAD-focused
    prompt to improve 2D floor plan image consistency.
    """
    print("\n==================================================")
    print("Generating Optimized Prompt using Vastu RAG Agent...")
    print("==================================================")

    qa_chain = get_qa_chain()

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

    rag_query = f"""
    Generate a compact architectural room placement mapping
    optimized for GPT-image-2 CAD floor plan rendering.

    IMPORTANT:
    - Keep output concise
    - No long explanations
    - No paragraphs
    - No markdown tables
    - No repeated rules

    FORMAT:

    GROUND FLOOR:
    - Room -> Position

    FIRST FLOOR:
    - Room -> Position

    SECOND FLOOR:
    - Room -> Position

    RULES:
    - Use visual positions:
    front-left
    front-right
    rear-left
    rear-right
    center-left
    center-right
    center

    - Kitchen adjacent to Dining
    - Parking in front facing side
    - Internal stairs only
    - Follow Vastu principles
    - Keep layout architecturally balanced

    PROJECT:
    - Plot: {plot_w}ft x {plot_l}ft
    - Facing: {facing}
    - Floors: {floors}
    - Bedrooms: {bedrooms}
    - Bathrooms: {bathrooms}
    - Building type: {building_type}
    - Features: {', '.join(feature_list)}
    - Layout preferences: {layout_pref}
    """

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
