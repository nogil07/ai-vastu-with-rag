import base64
import os
from datetime import datetime

from markdown_pdf import MarkdownPdf, Section


def _base_styles() -> str:
    return (
        "<style>\n"
        ":root {"
        "--ink:#1b2b3a; --muted:#536b7f; --accent:#2a84be; --accent-dark:#274861;"
        "--line:#d3dde6; --soft:#f7fbff; --page:#f1f3f5; --card:#ffffff;"
        "}\n"
        "body { font-family:'Segoe UI',Arial,sans-serif; color:var(--ink); font-size:11px; line-height:1.58; background:var(--page); }\n"
        "h1 { font-size:28px; margin:0; text-align:left; color:var(--accent-dark); font-weight:800; text-transform:uppercase; letter-spacing:.6px; }\n"
        "h2 { font-size:16px; margin:24px 0 10px; color:var(--accent); border-bottom:2px solid var(--line); padding-bottom:6px; font-weight:800; }\n"
        "h3 { font-size:13px; margin:16px 0 7px; color:#2f5978; }\n"
        "p { margin:8px 0; }\n"
        "ul,ol { margin:6px 0 10px 18px; }\n"
        "li { margin:4px 0; }\n"
        "table { width:100%; border-collapse:collapse; margin:10px 0 16px; font-size:10.5px; background:#fff; border:1px solid var(--line); }\n"
        "th, td { border:1px solid var(--line); padding:8px 10px; vertical-align:top; }\n"
        "th { background:var(--soft); color:#24455f; font-weight:700; }\n"
        "tr:nth-child(even) td { background:#fcfeff; }\n"
        "hr { border:0; border-top:1px solid var(--line); margin:18px 0; }\n"
        ".sheet { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:20px; }\n"
        ".title-block { border-top:4px solid var(--accent-dark); border-bottom:2px solid var(--accent-dark); padding:12px 8px 10px; margin-bottom:14px; }\n"
        ".title-sub { text-align:center; color:#35556f; font-size:14px; font-weight:700; margin-top:8px; }\n"
        ".meta { text-align:center; color:var(--muted); font-size:11px; margin-top:4px; }\n"
        ".img-wrap { border:1px solid var(--line); border-radius:8px; background:#fff; padding:10px; margin:12px 0 16px; }\n"
        ".img-wrap img { width:100%; height:auto; border-radius:6px; display:block; }\n"
        ".img-cap { text-align:center; color:var(--muted); font-size:10px; margin-top:6px; }\n"
        ".report-band { text-align:center; font-size:13px; font-weight:700; color:#273f53; margin:6px 0 2px; }\n"
        ".footer { text-align:center; color:#647a8b; font-size:10px; margin-top:16px; }\n"
        "</style>\n"
    )


def _header_block() -> str:
    today = datetime.now().strftime("%B %d, %Y")
    return (
        "<div class='title-block'>"
        "<h1>AUTOMATED VASTU SHASTRA AND KPBR AUDIT</h1>"
        "<div class='meta'>Generated on " + today + "</div>"
        "</div>"
        "<div class='report-band'>AI Vastu Compliance Report</div>"
        "<hr/>"
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
