import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

from user_input import generate_prompt_from_dict
from generate_image import main as run_generate_image
from generate_report import generate_vastu_report
from generate_pdf import generate_pdf_report
from rag_chatbot import setup_chatbot_rag

load_dotenv()

app = Flask(__name__)
# Enable CORS for the React frontend running on Vite (usually port 3000 or 5173)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global Chatbot RAG Chain
# We initialize this ONCE at server startup to prevent 10s PDF loading delays on every message.
print("\n--- Initializing Vasuttan AI Chatbot Memory ---")
chatbot_memory = setup_chatbot_rag()
if not chatbot_memory:
    print("Warning: Conversational Chatbot could not be loaded into memory.")
print("--- Server Ready! ---\n")

@app.route('/api/generate', methods=['POST'])
def generate_floor_plan():
    """
    Main orchestration endpoint.
    1. Receives JSON dict of form data
    2. Runs RAG to generate optimized prompt
    3. Generates the 2D layout image
    4. Generates the Vastu compliance report
    5. Combines them into a PDF
    """
    try:
        data = request.json
        print("\n[+] Received generation request from frontend:", data)
        
        # 1. Generate prompt
        print("[+] 1/4 - Generating prompt via RAG...")
        prompt = generate_prompt_from_dict(data)
        if not prompt:
            return jsonify({"error": "Failed to generate prompt from RAG system."}), 500
            
        # 2. Generate Image
        print("[+] 2/4 - Generating image via DALL-E...")
        image_success = run_generate_image()
        if not image_success:
            return jsonify({"error": "Failed to generate layout image."}), 500
            
        # 3. Generate Markdown Report
        print("[+] 3/4 - Generating Vastu report via Gemini...")
        report_success = generate_vastu_report()
        if not report_success:
            return jsonify({"error": "Failed to generate Vastu compliance report."}), 500
            
        # 4. Compile PDF
        print("[+] 4/4 - Compiling final PDF...")
        pdf_success = generate_pdf_report()
        if not pdf_success:
            return jsonify({"error": "Failed to compile the final PDF."}), 500
            
        print("[+] Pipeline complete! Successfully generated all assets.")
        return jsonify({
            "success": True, 
            "message": "Floor plan and report generated successfully!"
        })
        
    except Exception as e:
        print(f"Error in generation pipeline: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/download', methods=['GET'])
def download_pdf():
    try:
        pdf_path = os.path.join(os.getcwd(), 'Vastu_Floor_Plan_Report.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF report not found."}), 404
        return send_file(pdf_path, as_attachment=True, download_name="Vastu_Floor_Plan_Report.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/image', methods=['GET'])
def get_image():
    try:
        image_path = os.path.join(os.getcwd(), 'generated_floor_plan.png')
        if not os.path.exists(image_path):
            return jsonify({"error": "Generated image not found."}), 404
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/report', methods=['GET'])
def get_report():
    try:
        report_path = os.path.join(os.getcwd(), 'vastu_compliance_report.md')
        if not os.path.exists(report_path):
            return jsonify({"error": "Vastu report not found."}), 404
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/email', methods=['POST'])
def send_email():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name', 'User')
        
        if not email:
            return jsonify({"error": "Email address is required."}), 400
            
        pdf_path = os.path.join(os.getcwd(), 'Vastu_Floor_Plan_Report.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF report not found. Please generate a plan first."}), 404
            
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        
        if not sender_email or not sender_password:
            return jsonify({"error": "Email server not configured on backend."}), 500
            
        msg = EmailMessage()
        msg['Subject'] = 'Your Vastu AI Floor Plan Report'
        msg['From'] = sender_email
        msg['To'] = email
        msg.set_content(f"Hello {name},\n\nPlease find attached your AI-generated Vasuttan Floor Plan and Vastu Compliance Report.\n\nThank you for using Vasuttan AI!")
        
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Vastu_Floor_Plan_Report.pdf')
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        return jsonify({"success": True, "message": f"Email sent to {email}"})
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_vasuttan():
    """
    Receives a message string from the React Chat Widget.
    Passes it through the isolated `chatbot_memory` RAG chain and returns the response.
    """
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({"error": "Message is required."}), 400
        
    if not chatbot_memory:
        return jsonify({"error": "The Vasuttan AI agent is currently offline or failed to initialize."}), 500
        
    try:
        # The chain expects 'query' based on the standard RetrievalQA prompt setup
        response = chatbot_memory.invoke({"query": message})
        answer = response.get("result", "I'm sorry, I couldn't process that.")
        return jsonify({"reply": answer})
    except Exception as e:
        print(f"Chatbot pipeline error: {e}")
        return jsonify({"error": "An error occurred while Vasuttan was thinking."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
