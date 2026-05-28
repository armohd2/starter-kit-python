import os
import shutil
import time
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Receipts to Riches API")

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# POST /receipts
# Accepts a file upload and saves it to the /uploads directory.
# ---------------------------------------------------------------------------
@app.post("/receipts", status_code=201)
async def upload_receipt(receipt: UploadFile = File(...)):
    if receipt.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPG, PNG, WebP and PDF are accepted.",
        )

    filename = f"{int(time.time() * 1000)}-{receipt.filename}"
    dest = UPLOADS_DIR / filename

    with dest.open("wb") as f:
        shutil.copyfileobj(receipt.file, f)

    # -------------------------------------------------------------------------
    # TODO: AI EXTRACTION — plug in your OpenAI call here
    # -------------------------------------------------------------------------
    #
    # import base64
    # import json
    # from openai import OpenAI
    #
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    #
    # Step 1 — Read the saved file as base64
    # with open(dest, "rb") as f:
    #     image_base64 = base64.b64encode(f.read()).decode()
    #
    # Step 2 — Send to GPT-4o Vision and ask it to extract receipt fields
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[{
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "text",
    #                 "text": "Extract the following from this receipt and return as JSON: store_name, date, items (list of {name, price}), total_amount, category (e.g. groceries, dining, transport).",
    #             },
    #             {
    #                 "type": "image_url",
    #                 "image_url": {"url": f"data:{receipt.content_type};base64,{image_base64}"},
    #             },
    #         ],
    #     }],
    # )
    #
    # Step 3 — Parse the extracted JSON from the model response
    # receipt_data = json.loads(response.choices[0].message.content)
    #
    # Step 4 — Save to your database (design your own schema!)
    # e.g. db.save_receipt(filename=filename, **receipt_data)
    #
    # -------------------------------------------------------------------------

    return {"message": "Receipt uploaded successfully.", "filename": filename}


# ---------------------------------------------------------------------------
# GET /receipts
# Returns a list of files currently in /uploads.
# Once you have a database, replace this with a DB query.
# ---------------------------------------------------------------------------
@app.get("/receipts")
def list_receipts():
    files = [
        {"filename": f.name, "uploaded_at": f.stat().st_mtime}
        for f in UPLOADS_DIR.iterdir()
        if f.is_file()
    ]
    return files


# ---------------------------------------------------------------------------
# GET /insights
# Returns AI-generated spending insights.
# ---------------------------------------------------------------------------
@app.get("/insights")
def get_insights():
    # -------------------------------------------------------------------------
    # TODO: AI INSIGHTS — plug in your OpenAI call here
    # -------------------------------------------------------------------------
    #
    # import json
    # from openai import OpenAI
    #
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    #
    # Step 1 — Fetch all processed receipt data from your database
    # receipts = db.get_all_receipts()
    #
    # Step 2 — Ask GPT to analyse spending patterns across all receipts
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a personal finance advisor. Analyse the user's spending data and provide clear, actionable insights.",
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Here is my spending data: {json.dumps(receipts)}. Please provide: 1) a spending summary, 2) top spending categories, 3) three specific saving tips.",
    #         },
    #     ],
    # )
    #
    # Step 3 — Return the insights to the frontend
    # return {"insights": response.choices[0].message.content}
    #
    # -------------------------------------------------------------------------

    return {
        "message": "Insights endpoint placeholder — implement AI analysis here!",
        "insights": None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
