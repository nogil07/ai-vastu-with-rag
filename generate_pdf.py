import os
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
        "h2 { color: #3b82f6; border-bottom: 1px solid #e5e7eb; padding-bottom: 5px; }\n"
        "h1.main-title { color: #1e3a8a; text-align: center; font-size: 24px; }\n"
        "</style>\n\n"
        "<h1 class='main-title'>🏛️ AUTOMATED VASTU SHASTRA & KPBR AUDIT</h1>\n\n"
        "---\n\n"
    )
    
    if os.path.exists(img_file):
        # markdown_pdf can render local images via absolute path
        abs_img_path = os.path.abspath(img_file).replace('\\', '/')
        final_md += f"![Generated Floor Plan](file:///{abs_img_path})\n\n---\n\n"
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
