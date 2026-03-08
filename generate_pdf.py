import os
import base64
from markdown_pdf import MarkdownPdf, Section

def generate_pdf_report():
    """
    Combines the generated_floor_plan.png and vastu_compliance_report.md
    into a single beautifully styled PDF using markdown_pdf.
    """
    md_file = "vastu_compliance_report.md"
    img_file = "generated_floor_plan.png"
    out_file = "Vastu_Floor_Plan_Report.pdf"

    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found.")
        return False

    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Create the markdown text with embedded image if it exists
    final_md = (
        "<style>\n"
        "body { font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; font-size: 11px; background-color: #ffffff; }\n"
        "h1.main-title { color: #0f172a; text-align: center; font-size: 24px; font-weight: 800; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1.5px; }\n"
        "h2 { color: #1e40af; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 24px; font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }\n"
        "h3 { color: #334155; font-size: 13px; margin-top: 16px; font-weight: 600; }\n"
        "table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; font-size: 11px; border: 1px solid #cbd5e1; }\n"
        "th, td { border: 1px solid #cbd5e1; padding: 10px 14px; text-align: left; vertical-align: middle; }\n"
        "th { background-color: #f1f5f9; font-weight: 700; color: #0f172a; text-transform: uppercase; font-size: 10px; letter-spacing: 0.5px; }\n"
        "tr:last-child td { border-bottom: none; }\n"
        "tr:nth-child(even) { background-color: #fafafa; }\n"
        "li { margin-bottom: 6px; }\n"
        "p { margin-bottom: 10px; }\n"
        "hr { border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0; }\n"
        ".report-header { text-align: center; margin-bottom: 25px; padding: 20px; background-color: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; }\n"
        ".subtitle { color: #64748b; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }\n"
        ".image-container { text-align: center; margin: 25px 0; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #ffffff; }\n"
        ".image-container img { max-width: 100%; height: auto; border-radius: 4px; display: block; margin: 0 auto; }\n"
        "</style>\n\n"
        "<div class='report-header'>\n"
        "<h1 class='main-title'>🏛️ Automated Vastu & Architectural Audit</h1>\n"
        "<div class='subtitle'>Premium Master Plan Analysis</div>\n"
        "</div>\n\n"

        "---\n\n"
    )
    
    if os.path.exists(img_file):
        # markdown_pdf natively supports base64 embedded images, bypassing local path resolution issues.
        try:
            with open(img_file, "rb") as image_f:
                b64_img = base64.b64encode(image_f.read()).decode('utf-8')
            img_html = f"<img src='data:image/png;base64,{b64_img}' alt='Generated Floor Plan' />"
            final_md += f"<div class='image-container'>\n\n{img_html}\n\n</div>\n\n---\n\n"
        except Exception as e:
            print(f"Warning: Failed to encode image: {e}")
    else:
        print(f"Warning: {img_file} missing. PDF will not include the image.")
        
    final_md += md_text

    try:
        pdf = MarkdownPdf(toc_level=2)
        pdf.add_section(Section(final_md, toc=False))
        pdf.meta["title"] = "Vasuttan AI Report"
        pdf.meta["author"] = "Vasuttan"
        pdf.save(out_file)
        
        print(f"Successfully generated PDF: {out_file}")
        return True
    except Exception as e:
        print(f"Error generating PDF compilation: {e}")
        return False

if __name__ == "__main__":
    generate_pdf_report()
