# Receipts to Riches — Python Starter Kit

Hackathon Starter Kit | Theme: Receipts to Riches: Your AI Spending Sage

This is your starting point. It provides a working file upload backend and a React frontend. Your job is to build on top of it — add AI extraction, design your database, and generate meaningful spending insights.

---

## Project Structure

```
starter-kit-python/
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── UploadPage.jsx       Functional — uploads files to the backend
│       │   ├── ReceiptsPage.jsx     Placeholder — you build this
│       │   └── InsightsPage.jsx     Placeholder — you build this
│       └── services/
│           └── api.js               Axios API calls
└── backend/
    ├── main.py                      FastAPI server with upload and stub endpoints
    ├── uploads/                     Uploaded receipt files land here (auto-created)
    ├── requirements.txt
    └── .env.example
```

---

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Server starts on http://localhost:8000

Auto-generated API docs are available at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — you should be able to upload a file straight away.

---

## API Endpoints

| Method | Path        | Description                              |
|--------|-------------|------------------------------------------|
| POST   | /receipts   | Upload a receipt (JPG, PNG, PDF)         |
| GET    | /receipts   | List uploaded files                      |
| GET    | /insights   | Return AI-generated insights (stub)      |

---

## Adding AI

The `main.py` file contains clearly marked TODO blocks with pseudo-code showing where and how to plug in OpenAI.

Install the OpenAI SDK:

```bash
pip install openai
```

- **Receipt extraction** uses GPT-4o Vision — it reads the image or PDF and returns structured JSON (store name, items, total, category).
- **Spending insights** uses GPT-4o Chat — you pass it all extracted receipt data and ask for a spending summary, top categories, and saving tips.

Add your API key to `.env`:

```
OPENAI_API_KEY=sk-...
```

Note: GPT-4o Vision calls cost more than regular chat calls. Cache results in your database so you only process each receipt once.

---

## Database — Your Design Choice

The starter kit has no database by design — designing the schema is part of the challenge.

Recommended options:

| Option      | Best for                     | How to use                                         |
|-------------|------------------------------|----------------------------------------------------|
| SQLite      | Quick start, no setup        | Built into Python — use sqlite3 or SQLAlchemy      |
| PostgreSQL  | Production-ready, relational | pip install psycopg2-binary sqlalchemy             |
| MongoDB     | Flexible document store      | pip install pymongo                                |

Suggested fields to think about for a receipts table:
`id`, `filename`, `store_name`, `date`, `total_amount`, `category`, `items` (JSON), `uploaded_at`

---

## Ideas to Build

- Parse receipts with GPT-4o Vision and store structured data
- Build the Receipts page — list cards showing extracted data
- Build the Insights page — charts using Recharts or Chart.js
- Spending breakdown by category
- Monthly spend trend
- A chat interface letting users ask questions about their spending

---

## Useful Packages

Frontend:
- `recharts` — React charts
- `react-query` — data fetching with caching

Backend:
- `openai` — official OpenAI SDK
- `sqlalchemy` — ORM for SQLite or PostgreSQL
- `pypdf` or `pdfplumber` — extract text from PDFs before sending to GPT
