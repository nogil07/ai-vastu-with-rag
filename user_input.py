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
        reqs['groundFloorBedrooms'] = "0"

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
        "Create an highly attractive, fully rendered modern 2D CAD floor plan sheet (top view only).\n\n"
        "STYLE:\n"
        "- Pure white background outside plot, white inner floors with colored, realistic modern furniture.\n"
        "- Plot boundary filled with dense, realistic green grass and plants to clearly show setbacks. Car in driveway.\n\n"
        "COMPOSITION:\n"
        f"- Top center: '{facing.upper()}-FACING {building_type.upper()}' and '{int(plot_w)}ft x {int(plot_l)}ft PLOT'.\n"
        "- Ground Floor laid out left, First Floor alongside it.\n"
        "- Bottom Left: LEGEND (Walls/Doors/Windows). Bottom Right: VASTU COMPLIANCE box.\n\n"
        "PROJECT SPECIFICS:\n"
        f"- Plot Dimensions: {plot_w}ft x {plot_l}ft plot. (You MUST annotate outer plot dimensions {plot_w}ft and {plot_l}ft with arrows!).\n"
        f"- Rooms: {', '.join(feature_list) if feature_list else 'Standard'}.\n"
        f"{gf_rule_text}\n"
        "LAYOUT RULES (CRITICAL):\n"
        f"- ENTRANCES: Place a MAIN ENTRANCE with a text label '{facing.upper()} MAIN ENTRANCE' and an arrow. The side with the Main Entrance is considered the {facing.upper()} side.\n"
        "- ROUTING (CRITICAL FIX): Main Entrance MUST open DIRECTLY into a LIVING ROOM or LOBBY ONLY. Generating an entrance that opens into a BEDROOM, KITCHEN, or BATHROOM is a fatal failure.\n"
        "- STAIRCASE (MANDATORY): A Staircase MUST be clearly drawn starting on the Ground Floor and continuing on the First Floor.\n"
        "- EXITS: Provide an additional Secondary Exit / Back Door at the rear of the house.\n"
        "- Kitchen connected to dining. Bedrooms/toilets visually private from entrance.\n"
        "- Ensure practical, logical room placements.\n\n"
        "DETAILING & SETBACKS (CRITICAL):\n"
        "- Building must NOT touch plot walls. Must be visibly centered with green setbacks on all 4 sides.\n"
        "- Label 4 side clearances using 'SETBACK [value in m]' ON the green space (no front/rear/ft labels).\n"
        "- Wall thickness clearly shown. Doors have swing arcs (NO D1/D2 tags). Windows have NO W1/W2 tags.\n"
        "- ROOM LABELS: Every single room MUST have a large text label inside it (e.g. LIVING ROOM, KITCHEN, BEDROOM) + room dimensions.\n"
        f"- PLOT LABELS: Overall {plot_w}ft x {plot_l}ft dimensions must be drawn with arrowheads on the outer compound wall.\n\n"
        "VASTU/KPBR RULES:\n"
        f"{rule_block}\n\n"
        "DO NOT INCLUDE (FATAL ERRORS):\n"
        "- DO NOT MAKE THE KITCHEN THE ENTRANCE. The Main Entrance MUST NOT lead into the Kitchen under any circumstances.\n"
        "- NO 3D/Isometric. NO door/window measurement boxes (e.g., DO NOT show D1=4x7).\n"
        "- NO blurry text. No unlabelled rooms. NO missing stairs on Ground Floor.\n"
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
    prefer_gf = "Yes" if _yn(reqs.get("preferGroundFloorBedrooms", "No")) else "No"
    gf_bedrooms = int(_safe_num(reqs.get("groundFloorBedrooms", "0"), 0))

    rag_query = (
        "From Vastu and KPBR context, return ONLY concise CAD constraints for this residence. "
        "Use exactly these headings and short bullet points under each heading:\n"
        "1) VASTU_DIRECTION_RULES\n"
        "2) VASTU_ADJACENCY_RULES\n"
        "3) KPBR_SETBACK_RULES\n"
        "4) DO_NOT_PLACE_RULES\n"
        "5) DIMENSION_HINTS\n\n"
        f"Project details: {plot_w} ft x {plot_l} ft, {facing}-facing, {floors}, "
        f"{bedrooms} bedrooms ({gf_bedrooms} on GF: {prefer_gf}), {bathrooms} bathrooms, building type: {building_type}, "
        f"built-up area target: {built_up} sqft, layout preferences: {layout_pref}, architectural style: {style}, "
        f"vastu compliance preference: {vastu_level}.\n"
        "Keep response under 250 words. No preface and no conclusion."
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
