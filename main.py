from fastapi import FastAPI, Request
from models import TallyResponse
from notion_client import create_notion_page
import json

app = FastAPI()

@app.post("/submit")
async def submit_tally(data: TallyResponse):
    result = create_notion_page(data.dict())
    return result

@app.post("/webhook")
async def tally_webhook(request: Request):
    # Get the raw JSON data from Tally webhook
    payload = await request.json()
    
    # Extract the form data from the Tally webhook payload
    # The structure depends on how Tally formats their webhook data
    # This is a simplified example - you may need to adjust based on actual Tally webhook format
    form_data = payload.get("data", {}).get("formResponse", {})
    
    if not form_data:
        return {"success": False, "error": "Invalid webhook data"}
    
    # Map Tally fields to your model fields
    # This mapping should match your Tally form field IDs to your model field names
    # You'll need to inspect the actual webhook data to get the correct field IDs
    try:
        tally_data = {
            "이름": form_data.get("이름", ""),
            "날짜": form_data.get("날짜", ""),
            "시간": form_data.get("시간", ""),
            "연락처": form_data.get("연락처", ""),
            "학년": form_data.get("학년", ""),
            "입학_테스트_희망_시간": form_data.get("입학_테스트_희망_시간", None)
        }
        
        # Create a Notion page with the data
        result = create_notion_page(tally_data)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/zapier")
async def zapier_webhook(request: Request):
    """
    Endpoint for Zapier integration with Tally.
    
    Zapier can be configured to:
    1. Trigger on new Tally form submissions
    2. Format and send the data to this endpoint
    """
    try:
        # Get the data sent from Zapier
        payload = await request.json()
        
        # Zapier will send data in a more straightforward format
        # You can configure the exact mapping in Zapier
        tally_data = {
            "이름": payload.get("이름", ""),
            "날짜": payload.get("날짜", ""),
            "시간": payload.get("시간", ""),
            "연락처": payload.get("연락처", ""),
            "학년": payload.get("학년", ""),
            "입학_테스트_희망_시간": payload.get("입학_테스트_희망_시간", None)
        }
        
        # Create a Notion page with the data
        result = create_notion_page(tally_data)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}