from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import logging
from notion_client import create_notion_page, get_database_properties

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tally_webhook.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("tally-webhook")

app = FastAPI(title="Tally to Notion Webhook")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 Tally의 도메인으로 제한해야 함
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Notion 데이터베이스 속성 캐싱
notion_properties = None

def map_tally_to_notion(tally_data):
    """Tally 폼 데이터를 Notion 형식으로 매핑"""
    # Tally 웹훅은 다양한 형태로 데이터를 보낼 수 있음
    # formResponse 필드가 있다면 그 안에 데이터가 있을 수 있음
    if isinstance(tally_data, dict) and "formResponse" in tally_data:
        entry = tally_data["formResponse"]
    # 배열로 온 경우 첫 번째 항목 사용
    elif isinstance(tally_data, list) and len(tally_data) > 0:
        entry = tally_data[0]
    else:
        entry = tally_data
    
    # Tally의 특수 문자가 포함된 키 처리
    cleaned_entry = {}
    if isinstance(entry, dict):
        for key, value in entry.items():
            if isinstance(key, str):
                clean_key = key.replace('﻿"', '').replace('"', '')
                cleaned_entry[clean_key] = value
    else:
        logger.error(f"Unexpected data format: {type(entry)}")
        return {}
    
    # Notion에 보낼 데이터 구성
    data = {
        "이름": cleaned_entry.get("이름", ""),
        "연락처": cleaned_entry.get("연락처", ""),
        "학년": cleaned_entry.get("학년", ""),
        "날짜": cleaned_entry.get("상담 희망 날짜", ""),
        "시간": cleaned_entry.get("상담 희망 시간", ""),
    }
    
    # 학교 정보 추가
    if "학교" in cleaned_entry:
        data["학교"] = cleaned_entry["학교"]
    
    # 입학 테스트 정보 추가
    test_date = cleaned_entry.get("입학 테스트 희망 날짜", "")
    test_time = cleaned_entry.get("입학 테스트 희망 시간", "")
    
    if test_date:
        data["입학_테스트_날짜"] = test_date
    if test_time:
        data["입학_테스트_시간"] = test_time
    
    return data

async def process_webhook_data(data):
    """웹훅 데이터 처리 및 Notion에 업데이트"""
    global notion_properties
    
    try:
        # 데이터베이스 속성 가져오기 (캐시된 값이 없으면 새로 가져옴)
        if notion_properties is None:
            notion_properties = get_database_properties()
            
        # Tally 데이터를 Notion 형식으로 변환
        notion_data = map_tally_to_notion(data)
        logger.info(f"Mapped data: {json.dumps(notion_data, ensure_ascii=False)}")
        
        # Notion 페이지 생성
        result = create_notion_page(notion_data, notion_properties)
        
        if result["success"]:
            logger.info(f"Successfully created Notion page for {notion_data.get('이름', 'unknown')}")
            return True
        else:
            logger.error(f"Failed to create Notion page: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing webhook data: {str(e)}")
        return False

@app.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    """Tally Form 웹훅 엔드포인트"""
    try:
        # 요청 본문 읽기
        data = await request.json()
        logger.info(f"Received webhook data: {json.dumps(data, ensure_ascii=False)}")
        
        # 백그라운드에서 데이터 처리
        background_tasks.add_task(process_webhook_data, data)
        
        return JSONResponse(content={"status": "processing"}, status_code=202)
    
    except Exception as e:
        logger.error(f"Error receiving webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """서버 상태 확인 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # 로컬 개발 서버 실행
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 