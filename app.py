import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google_sheets import GoogleSheetsClient
from notion_client import NotionClient

# 환경 변수 로드
load_dotenv()

def main():
    # 클라이언트 초기화
    sheets_client = GoogleSheetsClient()
    notion_client = NotionClient()
    
    # 마지막 동기화 시간 초기화
    last_sync_time = datetime.min
    
    print("Tally-Google Sheets-Notion 동기화 시작...")
    
    while True:
        try:
            # 새로운 응답 확인
            new_responses = sheets_client.get_new_responses(last_sync_time)
            
            if new_responses:
                print(f"{len(new_responses)}개의 새로운 응답을 발견했습니다.")
                
                # 각 응답을 Notion에 추가
                for response in new_responses:
                    try:
                        notion_client.create_page(response)
                        print(f"응답이 Notion에 성공적으로 추가되었습니다: {response.get('Timestamp', 'N/A')}")
                    except Exception as e:
                        print(f"Notion에 응답 추가 중 오류 발생: {e}")
                
                # 마지막 동기화 시간 업데이트
                last_sync_time = sheets_client.get_latest_response_time()
            
            # 1분 대기
            time.sleep(60)
            
        except Exception as e:
            print(f"동기화 중 오류 발생: {e}")
            time.sleep(60)  # 오류 발생 시 1분 대기 후 재시도

if __name__ == "__main__":
    main() 