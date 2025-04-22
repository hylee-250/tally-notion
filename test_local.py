import uvicorn
import threading
from pyngrok import ngrok
import webbrowser
import time
import json
import requests
import os
from main import app
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Ngrok 설정
def setup_ngrok(port):
    # .env 파일에서 authtoken 가져오기
    ngrok_token = os.getenv("NGROK_AUTHTOKEN")
    
    if ngrok_token and ngrok_token != "your_ngrok_authtoken_here":
        # .env 파일에 설정된 토큰 사용
        print("환경 변수에서 ngrok 토큰을 불러옵니다...")
        ngrok.set_auth_token(ngrok_token)
    else:
        # 토큰이 설정되지 않았거나 기본값인 경우, 사용자에게 입력 요청
        print("ngrok authtoken이 설정되지 않았습니다.")
        print("https://dashboard.ngrok.com/get-started/your-authtoken 에서 토큰을 가져와 설정해주세요.")
        auth_token = input("ngrok authtoken을 입력하세요: ")
        ngrok.set_auth_token(auth_token)
        
        # 입력받은 토큰을 .env 파일에 저장할지 물어보기
        save_token = input("이 토큰을 .env 파일에 저장하시겠습니까? (y/n): ")
        if save_token.lower() == 'y':
            with open('.env', 'r') as file:
                env_content = file.read()
            
            # 기존 NGROK_AUTHTOKEN 라인 교체
            if 'NGROK_AUTHTOKEN=' in env_content:
                env_content = env_content.replace(
                    f"NGROK_AUTHTOKEN={os.getenv('NGROK_AUTHTOKEN', 'your_ngrok_authtoken_here')}", 
                    f"NGROK_AUTHTOKEN={auth_token}"
                )
            else:
                # 없으면 추가
                env_content += f"\nNGROK_AUTHTOKEN={auth_token}"
            
            with open('.env', 'w') as file:
                file.write(env_content)
            print(".env 파일에 토큰이 저장되었습니다.")
    
    # Ngrok HTTP 터널 설정
    public_url = ngrok.connect(port)
    # URL 형식 올바르게 수정
    public_url_str = str(public_url).split('"')[1] if '"' in str(public_url) else str(public_url)
    print(f"ngrok 터널이 생성되었습니다: {public_url}")
    return public_url_str

# 테스트 데이터 전송 함수
def send_test_data(url):
    print("\n테스트 데이터를 전송합니다...")
    test_data = {
        "이름": "테스트 사용자",
        "날짜": "Apr 10, 2025",
        "시간": "12:30",
        "연락처": "010-1234-5678",
        "학년": "고등학교 1학년",
        "입학_테스트_희망_시간": None
    }
    
    try:
        response = requests.post(f"{url}/zapier", json=test_data)
        print(f"응답 상태 코드: {response.status_code}")
        print(f"응답 내용: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.json()
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

# 메인 함수
def main():
    # FastAPI 서버 포트
    port = 8000
    
    # 백그라운드에서 FastAPI 서버 실행
    server_thread = threading.Thread(
        target=uvicorn.run,
        kwargs={"app": app, "host": "127.0.0.1", "port": port}
    )
    server_thread.daemon = True
    server_thread.start()
    
    # 서버가 시작될 시간을 줌
    time.sleep(2)
    
    try:
        # Ngrok 설정
        public_url = setup_ngrok(port)
        
        print("\n===== 테스트 안내 =====")
        print(f"1. Zapier Webhook URL: {public_url}/zapier")
        print(f"2. 테스트용 웹훅 URL: {public_url}/webhook")
        print(f"3. API 기본 URL: {public_url}")
        print("4. 이 URL을 Zapier의 Webhook 설정에서 사용하거나")
        print("5. 테스트 버튼을 누르면 Notion에 테스트 데이터를 직접 보낼 수 있습니다.")
        
        # 테스트용 엔드포인트 확인
        print("\n=== 사용 가능한 엔드포인트 ===")
        print("- /zapier")
        print("- /webhook")
        print("- /submit")
        
        while True:
            print("\n=== 옵션 ===")
            print("1: URL 다시 보기")
            print("2: 테스트 데이터 보내기")
            print("3: 종료")
            
            choice = input("선택하세요 (1-3): ")
            
            if choice == "1":
                print(f"Zapier Webhook URL: {public_url}/zapier")
            elif choice == "2":
                # 사용자에게 엔드포인트 선택 옵션 제공
                print("\n데이터를 보낼 엔드포인트 선택:")
                print("1: /zapier")
                print("2: /webhook")
                print("3: /submit")
                endpoint_choice = input("선택하세요 (기본값: 1): ") or "1"
                
                if endpoint_choice == "1":
                    endpoint = "/zapier"
                elif endpoint_choice == "2":
                    endpoint = "/webhook"
                elif endpoint_choice == "3":
                    endpoint = "/submit"
                else:
                    endpoint = "/zapier"
                
                send_test_data(f"{public_url}{endpoint}")
            elif choice == "3":
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")
    
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
    finally:
        # Ngrok 터널 종료
        ngrok.kill()

if __name__ == "__main__":
    main() 