import base64
import os
from datetime import datetime

from markdown_pdf import MarkdownPdf, Section


def _base_styles() -> str:
    return (
        "<style>\n"
        ":root {"
        "--ink:#333333; --muted:#555555; --primary:#2b3d4f; --accent:#3b82f6;"
        "}\n"
        "body { font-family:'Arial',sans-serif; color:var(--ink); font-size:11px; line-height:1.6; background:#fff; margin:0; padding:0; }\n"
        "h2 { font-size:16px; margin:28px 0 12px; color:var(--accent); font-weight:bold; }\n"
        "p { margin:10px 0; color:var(--ink); }\n"
        "ul,ol { margin:8px 0 16px 20px; color:var(--ink); }\n"
        "li { margin:6px 0; line-height:1.5; }\n"
        "strong { color:var(--ink); font-weight:bold; }\n"
        ".sheet { padding:15px 25px; }\n"
        ".header { border-top:2px solid var(--primary); border-bottom:2px solid var(--primary); text-align:center; padding:12px 0; margin-bottom:20px; }\n"
        ".header-title { color:var(--primary); font-size:18px; font-weight:bold; margin:0; text-transform:uppercase; letter-spacing:0.5px; }\n"
        ".img-wrap { border:1px solid #ddd; padding:8px; margin:20px 0; text-align:center; background:#fff; }\n"
        ".img-wrap img { max-width:100%; height:auto; display:block; margin:0 auto; }\n"
        ".footer { text-align:center; color:var(--muted); font-size:10px; border-top:1px solid #ddd; padding-top:10px; margin-top:30px; }\n"
        "</style>\n"
    )


def _header_block() -> str:
    return (
        "<div class='header' style='margin-bottom: 20px;'>"
        "<h1 class='header-title'>&#127963; AUTOMATED VASTU SHASTRA & KPBR AUDIT</h1>"
        "</div>"
    )


def _image_block(img_file: str) -> str:
    if not os.path.exists(img_file):
        return ""
    try:
        with open(img_file, "rb") as image_f:
            b64_img = base64.b64encode(image_f.read()).decode("utf-8")
        return (
            "<div class='img-wrap'>"
            f"<img src='data:image/png;base64,{b64_img}' alt='Generated Floor Plan'/>"
            "</div>"
            "<div class='header' style='margin-top: 40px; margin-bottom: 20px;'>"
            "<h1 class='header-title' style='text-transform:none; font-size:20px;'>&#128214; AI Vastu Compliance Report</h1>"
            "</div>"
        )
    except Exception as e:
        print(f"Warning: failed to embed image: {e}")
        return ""


def generate_pdf_report() -> bool:
    md_file = "vastu_compliance_report.md"
    img_file = "generated_floor_plan.png"
    out_file = "Vastu_Floor_Plan_Report.pdf"

    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found.")
        return False

    with open(md_file, "r", encoding="utf-8") as f:
        report_md = f.read().strip()

    final_md = (
        _base_styles()
        + "<div class='sheet'>"
        + _header_block()
        + _image_block(img_file)
        + report_md
        + "<div class='footer'>Prepared by Vastu AI � Preliminary Compliance Audit</div>"
        + "</div>"
    )

    try:
        pdf = MarkdownPdf(toc_level=2)
        pdf.add_section(Section(final_md, toc=False))
        pdf.meta["title"] = "Automated Vastu Shastra and KPBR Audit"
        pdf.meta["author"] = "Vastu AI"
        pdf.save(out_file)
        print(f"Successfully generated PDF: {out_file}")
        return True
    except Exception as e:
        print(f"Error generating PDF compilation: {e}")
        return False


if __name__ == "__main__":
    generate_pdf_report()
