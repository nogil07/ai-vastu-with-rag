from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

from user_input import generate_prompt_from_dict
from generate_image import main as generate_image_main
from generate_report import generate_vastu_report
from generate_pdf import generate_pdf_report
from rag_chatbot import get_chatbot_response

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"status": "error", "detail": "Empty query"}), 400
        
        response = get_chatbot_response(query)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        print(f"Chatbot error: {e}")
        return jsonify({"status": "error", "detail": str(e)}), 500

@app.route("/api/generate", methods=["POST"])
def generate_plan():
    try:
        req_dict = request.get_json()
        if not req_dict:
            return jsonify({"status": "error", "detail": "Invalid JSON mapping"}), 400

        # Map React specific keys to python backend keys expected by user_input.py
        req_dict['preferGroundFloorBedrooms'] = "Yes" if req_dict.get('groundFloorBedroom') else "No"
        req_dict['facing'] = req_dict.get('plotFacing', 'East')
        req_dict['vastuCompliance'] = req_dict.get('vastuLevel', 'High')
        req_dict['layoutPreferences'] = req_dict.get('layoutPrefs', 'Open Kitchen, Internal Stairs')
        req_dict['style'] = req_dict.get('archStyle', 'Modern')
        
        # Convert booleans to "Yes"/"No" strings expected by backend
        for key in ['kitchen', 'livingRoom', 'diningArea', 'poojaRoom', 'studyRoom', 'parking']:
            if isinstance(req_dict.get(key), bool):
                req_dict[key] = "Yes" if req_dict[key] else "No"

        # Write requirements
        reqs_file = "last_user_requirements.json"
        with open(reqs_file, "w", encoding="utf-8") as f:
            json.dump(req_dict, f, indent=2)

        print("--- 1. Generating Prompt from RAG ---")
        prompt = generate_prompt_from_dict(req_dict)
        if not prompt:
            return jsonify({"status": "error", "detail": "Failed to generate prompt from RAG"}), 500

        print("--- 2. Generating Image ---")
        img_ok = generate_image_main()
        if not img_ok:
            return jsonify({"status": "error", "detail": "Failed to generate image"}), 500

        print("--- 3. Generating Vastu Report ---")
        report_ok = generate_vastu_report()
        if not report_ok:
            return jsonify({"status": "error", "detail": "Failed to generate text report"}), 500

        print("--- 4. Generating PDF ---")
        pdf_ok = generate_pdf_report()
        if not pdf_ok:
            return jsonify({"status": "error", "detail": "Failed to generate PDF"}), 500

        return jsonify({"status": "success", "message": "Generation complete"})
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"status": "error", "detail": str(e)}), 500

@app.route("/api/result/image", methods=["GET"])
def get_image():
    if os.path.exists("generated_floor_plan.png"):
        return send_file("generated_floor_plan.png", mimetype='image/png')
    return jsonify({"status": "error", "detail": "Image not found"}), 404

@app.route("/api/result/report", methods=["GET"])
def get_report():
    if os.path.exists("vastu_compliance_report.md"):
        with open("vastu_compliance_report.md", "r", encoding="utf-8") as f:
            return jsonify({"markdown": f.read()})
    return jsonify({"status": "error", "detail": "Report not found"}), 404

@app.route("/api/result/pdf", methods=["GET"])
def get_pdf():
    pdf_path = "Vastu_Floor_Plan_Report.pdf"
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name="Vastu_Floor_Plan_Report.pdf", mimetype='application/pdf')
    return jsonify({"status": "error", "detail": "PDF not found"}), 404

@app.route("/api/email", methods=["POST"])
def send_email():
    try:
        req_data = request.get_json()
        if not req_data:
            return jsonify({"status": "error", "detail": "Missing JSON data"}), 400
            
        full_name = req_data.get("fullName")
        email_addr = req_data.get("email")
        
        if not full_name or not email_addr:
            return jsonify({"status": "error", "detail": "Missing fullName or email"}), 400

        pdf_path = "Vastu_Floor_Plan_Report.pdf"
        if not os.path.exists(pdf_path):
            return jsonify({"status": "error", "detail": "PDF not found to email"}), 404

        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")
        print(f"DEBUG: Attempting to send email via {sender}")
        host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        port = int(os.getenv("SMTP_PORT", 587))

        if not sender or not password:
            print(f"Mock Email sent to {email_addr} for {full_name}")
            return jsonify({"status": "success", "message": "Simulated email sent successfully (no SMTP credentials configured)"})

        msg = EmailMessage()
        msg['Subject'] = 'Your AI Vastu Floor Plan & Report'
        msg['From'] = sender
        msg['To'] = email_addr
        msg.set_content(f"Hello {full_name},\n\nPlease find attached your generated Vastu Floor Plan and Compliance Report.\n\nBest,\nAI Vastu Team")

        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename="Vastu_Floor_Plan_Report.pdf")

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        return jsonify({"status": "success", "message": "Email sent successfully"})
    except Exception as e:
        import traceback
        print(f"Error sending email: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "detail": f"Failed to send email: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
