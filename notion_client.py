import httpx
import os
from dotenv import load_dotenv
from utils import combine_date_time

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_page(data: dict):
    full_datetime = combine_date_time(data["날짜"], data["시간"])
    
    # Prepare properties for Notion
    properties = {
        "이름": {
            "title": [{
                "text": {"content": data["이름"]}
            }]
        },
        "희망 시간": {
            "date": {
                "start": full_datetime
            }
        },
        "연락처": {
            "phone_number": data["연락처"]
        },
        "학년": {
            "rich_text": [{
                "text": {"content": data["학년"]}
            }]
        }
    }
    
    # Add 입학 테스트 희망 시간 if provided
    if data.get("입학_테스트_희망_시간"):
        properties["입학 테스트 희망 시간"] = {
            "date": {
                "start": data["입학_테스트_희망_시간"]
            }
        }
    
    page_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": properties
    }

    response = httpx.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=page_data
    )

    if response.status_code in (200, 201):
        return {"success": True, "notion_response": response.json()}
    else:
        return {"success": False, "error": response.text}