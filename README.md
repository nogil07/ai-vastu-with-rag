# AI Vastu | https://ai-vastu-with-rag.vercel.app/ |

AI Vastu is a full-stack floor-plan generation app that combines Vastu Shastra, Kerala Panchayat Building Rules (KPBR), retrieval-augmented generation, AI image generation, and a polished React interface. Users enter plot and room requirements, the backend retrieves relevant Vastu/KPBR constraints, generates an optimized prompt, creates a floor-plan image, writes a compliance report, and exports a downloadable PDF.

## Features

- AI-assisted Vastu-compliant floor-plan generation
- KPBR and Vastu rule retrieval from bundled PDF documents
- RAG-powered prompt optimization using LangChain, Chroma, Hugging Face embeddings, and Gemini
- OpenAI image generation for 2D CAD-style floor plans
- Markdown compliance report generation
- PDF report export with embedded generated floor plan
- Email delivery endpoint for generated reports
- Floating RAG chatbot for Vastu/KPBR questions
- React + Vite frontend with 3D hero model, animated demo, dark mode, form wizard, result viewer, and report preview

## Tech Stack

### Backend

- Python
- Flask
- Flask-CORS
- LangChain
- ChromaDB
- Hugging Face sentence-transformer embeddings
- Google Gemini via `langchain-google-genai`
- OpenAI Images API
- PyMuPDF and RapidOCR for PDF text/OCR extraction
- `markdown-pdf` for PDF export

### Frontend

- React 19
- Vite
- TypeScript
- Tailwind CSS
- Three.js with React Three Fiber and Drei
- Motion
- Lenis smooth scrolling
- Lucide React icons
- React Markdown

## Project Structure

```text
.
|-- app.py                         # Flask API server
|-- user_input.py                  # RAG prompt construction and CLI input flow
|-- rag_vastu.py                   # Vastu/KPBR RAG setup for generation
|-- rag_chatbot.py                 # Dedicated chatbot RAG pipeline
|-- generate_image.py              # OpenAI image generation
|-- generate_report.py             # Gemini compliance report generation
|-- generate_pdf.py                # PDF compilation
|-- requirements.txt               # Python dependencies
|-- vastu-for-home.pdf             # Vastu reference document
|-- LSGD-KPBR-Amendment.pdf        # KPBR reference document
|-- db/                            # Generated Chroma vector DB for planner RAG
|-- db_chatbot/                    # Generated Chroma vector DB for chatbot RAG
|-- generated_floor_plan.png       # Latest generated plan image
|-- vastu_compliance_report.md     # Latest generated Markdown report
|-- Vastu_Floor_Plan_Report.pdf    # Latest generated PDF report
`-- frontend/
    |-- package.json
    |-- vite.config.ts
    |-- index.html
    |-- public/
    |   |-- Bambo_House.obj
    |   |-- vasuttan2.mp4
    |   `-- genereated_plan.jpeg
    `-- src/
        |-- App.tsx
        |-- main.tsx
        |-- index.css
        `-- components/
            |-- PlanForm.tsx
            |-- ResultView.tsx
            |-- Chatbot.tsx
            |-- Hero3D.tsx
            |-- ProductDemo.tsx
            `-- EmailModal.tsx
```

## Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- OpenAI API key with image-generation access
- Google Gemini API key

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite

# Optional, only needed for real email delivery.
EMAIL_USER=your_email_address
EMAIL_PASS=your_email_or_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

If email credentials are not configured, the backend simulates a successful email response.

## Backend Setup

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The Flask server runs on:

```text
http://localhost:8080
```

On first RAG usage, the app creates local Chroma vector stores under `db/` and `db_chatbot/`. This can take some time because PDFs may be parsed with OCR and embedding models may be downloaded.

## Frontend Setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite app runs on:

```text
http://localhost:3000
```

The frontend currently calls the backend at `http://localhost:8080`, so keep both servers running during local development.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/generate` | Generates the optimized prompt, floor-plan image, Markdown report, and PDF |
| `GET` | `/api/result/image` | Returns `generated_floor_plan.png` |
| `GET` | `/api/result/report` | Returns the Markdown compliance report as JSON |
| `GET` | `/api/result/pdf` | Downloads `Vastu_Floor_Plan_Report.pdf` |
| `POST` | `/api/chat` | Sends a Vastu/KPBR question to the chatbot RAG pipeline |
| `POST` | `/api/email` | Emails the generated PDF report or simulates delivery if SMTP is not configured |

Example generation request:

```json
{
  "plotLength": "40",
  "plotWidth": "30",
  "plotShape": "Rectangle",
  "plotFacing": "East",
  "floors": "G+1",
  "builtUpArea": "1200",
  "buildingType": "Independent house",
  "bedrooms": "3",
  "bathrooms": "3",
  "kitchen": true,
  "livingRoom": true,
  "diningArea": true,
  "poojaRoom": true,
  "studyRoom": false,
  "parking": true,
  "groundFloorBedroom": false,
  "vastuLevel": "High",
  "layoutPrefs": "Open Kitchen, Internal Stairs",
  "archStyle": "Modern",
  "outputFormat": "2D Floor Plan"
}
```

## Generation Flow

1. The React form posts user requirements to `/api/generate`.
2. Flask normalizes frontend field names for the Python pipeline.
3. `user_input.py` retrieves Vastu/KPBR rules and creates an optimized CAD prompt.
4. `generate_image.py` calls OpenAI image generation and saves `generated_floor_plan.png`.
5. `generate_report.py` uses Gemini to produce `vastu_compliance_report.md`.
6. `generate_pdf.py` embeds the image and report into `Vastu_Floor_Plan_Report.pdf`.
7. The frontend displays the generated image, rendered Markdown report, download button, and email modal.

## Generated Files

The app writes these files during generation:

- `last_user_requirements.json`
- `optimized_prompt_output.txt`
- `generated_floor_plan.png`
- `vastu_compliance_report.md`
- `Vastu_Floor_Plan_Report.pdf`
- `db/`
- `db_chatbot/`

These are runtime/generated artifacts. Keep only intentional sample outputs in version control.

## Notes

- The included PDFs are used as the knowledge base for Vastu and KPBR retrieval.
- The backend expects valid API keys for real generation and reporting.
- The first run may be slower because embeddings and vector stores are initialized.
- The current frontend is configured for local backend URLs. Update the fetch URLs before deploying to production.


