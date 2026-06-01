import base64
import json
import os
import shutil
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="ReceiptIQ API")

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

DB_FILE = Path("receipts.json")
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_db():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text())
    return []


def write_db(data):
    DB_FILE.write_text(json.dumps(data, indent=2))


def file_to_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


@app.get("/")
def home():
    return {"message": "ReceiptIQ backend is running"}


@app.post("/receipts", status_code=201)
async def upload_receipt(receipt: UploadFile = File(...)):
    if receipt.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, and WebP receipt images are supported for AI extraction."
        )

    filename = f"{int(time.time() * 1000)}-{receipt.filename}"
    file_path = UPLOADS_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(receipt.file, buffer)

    image_base64 = file_to_base64(file_path)

    prompt = """
    Extract receipt data from this image.

    Return ONLY valid JSON in this exact structure:
    {
      "store_name": "",
      "date": "",
      "currency": "GBP",
      "total_amount": 0,
      "category": "",
      "items": [
        {
          "name": "",
          "price": 0,
          "quantity": 1,
          "health_category": "healthy | moderate | unhealthy | non_food"
        }
      ],
      "summary": "",
      "saving_tip": ""
    }
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an AI receipt extraction assistant. Return only clean JSON."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{receipt.content_type};base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )

    extracted_data = json.loads(response.choices[0].message.content)

    record = {
        "id": int(time.time() * 1000),
        "filename": filename,
        "uploaded_at": time.time(),
        **extracted_data
    }

    receipts = read_db()
    receipts.append(record)
    write_db(receipts)
    print(record)

    return {
        "message": "Receipt uploaded and analysed successfully.",
        "receipt": record
    }


@app.get("/receipts")
def get_receipts():
    return read_db()


@app.get("/summary")
def get_summary():
    receipts = read_db()

    total_spent = sum(float(r.get("total_amount", 0)) for r in receipts)

    categories = {}
    stores = {}

    for receipt in receipts:
        category = receipt.get("category", "Other")
        store = receipt.get("store_name", "Unknown")

        categories[category] = categories.get(category, 0) + float(receipt.get("total_amount", 0))
        stores[store] = stores.get(store, 0) + float(receipt.get("total_amount", 0))

    return {
        "total_spent": round(total_spent, 2),
        "receipt_count": len(receipts),
        "categories": categories,
        "stores": stores
    }


@app.get("/insights")
def get_insights():
    receipts = read_db()

    if not receipts:
        return {
            "summary": "Upload your first receipt to unlock personalised insights.",
            "insights": []
        }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an encouraging AI financial coach. Be short, helpful, and user-friendly."
            },
            {
                "role": "user",
                "content": f"""
                Analyse these receipts and return JSON:
                {json.dumps(receipts)}

                Return:
                {{
                  "financial_twin": "",
                  "summary": "",
                  "insights": [
                    {{"title": "", "message": "", "type": "saving | warning | positive"}}
                  ],
                  "budget_prediction": "",
                  "health_summary": "",
                  "saving_opportunity": ""
                }}
                """
            }
        ]
    )

    return json.loads(response.choices[0].message.content)


@app.get("/bills")
def get_bills():
    return [
        {"name": "Car insurance", "amount": 89.00, "category": "Insurance"},
        {"name": "Gym membership", "amount": 24.99, "category": "Gym"},
        {"name": "Phone bill", "amount": 35.00, "category": "Phone"},
        {"name": "Netflix", "amount": 10.99, "category": "Subscription"},
        {"name": "Spotify Student", "amount": 5.99, "category": "Subscription"}
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
