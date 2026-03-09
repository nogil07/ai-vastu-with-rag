import base64
import os
from datetime import datetime

from markdown_pdf import MarkdownPdf, Section


def _base_styles() -> str:
    return (
        "<style>\n"
        ":root {"
        "--ink:#1a1a1a; --muted:#666666; --accent:#C7A15E; --accent-dark:#8A6D3B;"
        "--line:#e5e5e5; --soft:#fafafa; --page:#ffffff; --card:#ffffff;"
        "}\n"
        "body { font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; color:var(--ink); font-size:12px; line-height:1.6; background:var(--page); }\n"
        "h1 { font-size:26px; margin:0 0 8px 0; text-align:left; color:var(--ink); font-weight:700; text-transform:uppercase; letter-spacing:1px; }\n"
        "h2 { font-size:16px; margin:28px 0 12px; color:var(--accent-dark); border-bottom:1px solid var(--line); padding-bottom:8px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }\n"
        "h3 { font-size:14px; margin:20px 0 8px; color:var(--ink); font-weight:600; }\n"
        "p { margin:10px 0; color:var(--muted); }\n"
        "ul,ol { margin:8px 0 16px 20px; color:var(--muted); }\n"
        "li { margin:6px 0; line-height:1.5; }\n"
        "strong { color:var(--ink); font-weight:600; }\n"
        "hr { border:0; border-top:1px solid var(--line); margin:24px 0; }\n"
        ".sheet { background:var(--card); padding:30px 40px; }\n"
        ".title-block { border-left:4px solid var(--accent); padding-left:16px; margin-bottom:24px; }\n"
        ".meta { color:var(--muted); font-size:11px; margin-top:6px; text-transform:uppercase; letter-spacing:0.5px; }\n"
        ".img-wrap { border:1px solid var(--line); padding:12px; margin:24px 0; background:var(--soft); }\n"
        ".img-wrap img { width:100%; height:auto; display:block; border-radius:4px; }\n"
        ".img-cap { text-align:center; color:var(--muted); font-size:10px; margin-top:10px; text-transform:uppercase; letter-spacing:1px; }\n"
        ".report-band { font-size:12px; font-weight:600; color:var(--accent-dark); margin:0; text-transform:uppercase; letter-spacing:0.5px; }\n"
        ".footer { text-align:center; color:var(--muted); font-size:10px; border-top:1px solid var(--line); padding-top:16px; margin-top:32px; text-transform:uppercase; letter-spacing:1px; }\n"
        "</style>\n"
    )


def _header_block() -> str:
    today = datetime.now().strftime("%B %d, %Y")
    return (
        "<div class='title-block'>"
        "<div class='report-band'>AI Vastu Compliance Report</div>"
        "<h1>Automated Vastu & KPBR Audit</h1>"
        "<div class='meta'>Generated on " + today + "</div>"
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
            "<div class='img-cap'>GENERATED FLOOR PLAN SHEET</div>"
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
