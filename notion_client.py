import httpx
import os
import json
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

def get_database_properties():
    """Get the properties of the Notion database to see the correct property names"""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"
    response = httpx.get(url, headers=headers)
    
    if response.status_code == 200:
        database_info = response.json()
        properties = database_info.get("properties", {})
        print("\nAvailable properties in Notion database:")
        for prop_name, prop_details in properties.items():
            print(f"  - {prop_name} ({prop_details.get('type', 'unknown type')})")
        return properties
    else:
        print(f"Error retrieving database properties: {response.status_code}")
        print(response.text)
        return {}

def create_notion_page(data: dict, database_properties=None):
    if database_properties is None:
        database_properties = get_database_properties()
    
    full_datetime = combine_date_time(data["날짜"], data["시간"])
    
    # Base properties that should exist in any Notion database
    properties = {}
    
    # Find title property (the primary property in Notion)
    title_prop = None
    for prop_name, prop_details in database_properties.items():
        if prop_details.get("type") == "title":
            title_prop = prop_name
            break
    
    if title_prop:
        properties[title_prop] = {
            "title": [{
                "text": {"content": data["이름"]}
            }]
        }
    else:
        properties["이름"] = {
            "title": [{
                "text": {"content": data["이름"]}
            }]
        }
    
    # Add properties based on their type in the database
    for prop_name, prop_details in database_properties.items():
        prop_type = prop_details.get("type")
        
        # Skip the title property as we've already handled it
        if prop_type == "title":
            continue
        
        # Handle property based on its type
        if prop_name == "연락처" and prop_type == "phone_number":
            properties[prop_name] = {"phone_number": data["연락처"]}
        
        elif prop_name == "학년" and prop_type == "rich_text":
            properties[prop_name] = {
                "rich_text": [{
                    "text": {"content": data["학년"]}
                }]
            }
        
        elif prop_name == "학교" and prop_type == "rich_text" and data.get("학교"):
            properties[prop_name] = {
                "rich_text": [{
                    "text": {"content": data["학교"]}
                }]
            }
        
        elif prop_name == "상담 희망 날짜" and prop_type == "date":
            properties[prop_name] = {
                "date": {
                    "start": data["날짜"]
                }
            }
        
        elif prop_name == "상담 시간" and prop_type == "rich_text":
            properties[prop_name] = {
                "rich_text": [{
                    "text": {"content": data["시간"]}
                }]
            }
        
        elif prop_name == "입학 테스트 희망 날짜" and prop_type == "date" and data.get("입학_테스트_날짜"):
            properties[prop_name] = {
                "date": {
                    "start": data["입학_테스트_날짜"]
                }
            }
        
        elif prop_name == "입학 테스트 시간" and prop_type == "rich_text" and data.get("입학_테스트_시간"):
            properties[prop_name] = {
                "rich_text": [{
                    "text": {"content": data["입학_테스트_시간"]}
                }]
            }
    
    page_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": properties
    }

    print(f"Sending data to Notion: {json.dumps(page_data, indent=2, ensure_ascii=False)}")
    
    response = httpx.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=page_data
    )

    if response.status_code in (200, 201):
        return {"success": True, "notion_response": response.json()}
    else:
        error_detail = response.text
        print(f"Error response from Notion API (Status {response.status_code}):")
        print(error_detail)
        return {"success": False, "error": error_detail}

def process_json_file(json_file_path):
    print(f"Reading JSON file: {json_file_path}")
    with open(json_file_path, 'r', encoding='utf-8') as file:
        entries = json.load(file)
    
    print(f"Found {len(entries)} entries in the JSON file")
    
    # Get database properties once to reuse
    database_properties = get_database_properties()
    
    results = []
    for entry in entries:
        # Handle weird characters in keys if they exist
        cleaned_entry = {}
        for key, value in entry.items():
            clean_key = key.replace('﻿"', '').replace('"', '')
            cleaned_entry[clean_key] = value
        
        print(f"Processing entry: {json.dumps(cleaned_entry, indent=2, ensure_ascii=False)}")
        
        data = {
            "이름": cleaned_entry["이름"],
            "연락처": cleaned_entry["연락처"],
            "학년": cleaned_entry["학년"],
            "날짜": cleaned_entry.get("상담 희망 날짜", ""),
            "시간": cleaned_entry.get("상담 희망 시간", "")
        }
        
        # Add 학교 if it exists
        if "학교" in cleaned_entry:
            data["학교"] = cleaned_entry["학교"]
        
        # Process 입학 테스트 희망 시간 if it exists and is not empty
        test_date = cleaned_entry.get("입학 테스트 희망 날짜", "")
        test_time = cleaned_entry.get("입학 테스트 희망 시간", "")
        if test_date:
            data["입학_테스트_날짜"] = test_date
        if test_time:
            data["입학_테스트_시간"] = test_time
        
        print(f"Prepared data for Notion: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Create the Notion page
        result = create_notion_page(data, database_properties)
        results.append({
            "name": data["이름"],
            "success": result["success"],
            "error": result.get("error")
        })
    
    return results

if __name__ == "__main__":
    # Check environment variables
    print(f"NOTION_TOKEN set: {'Yes' if NOTION_TOKEN else 'No'}")
    print(f"NOTION_DATABASE_ID set: {'Yes' if NOTION_DATABASE_ID else 'No'}")
    
    # Example usage
    json_file_path = "response/sub1.json"
    results = process_json_file(json_file_path)
    print(f"\nProcessed {len(results)} entries:")
    for result in results:
        status = "Success" if result["success"] else "Failed"
        print(f"{result['name']}: {status}")
        if not result["success"] and "error" in result:
            print(f"  Error: {result['error'][:200]}...")
            print(f"  Error: {result['error'][:200]}...")