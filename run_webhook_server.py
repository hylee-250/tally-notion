#!/usr/bin/env python3
import subprocess
import sys
import time
import os
import signal
import json
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def check_requirements():
    """필요한 패키지가 설치되어 있는지 확인"""
    try:
        import uvicorn
        import fastapi
        import pyngrok
    except ImportError as e:
        print(f"필요한 패키지가 설치되어 있지 않습니다: {e}")
        print("pip install -r requirements.txt 명령어로 필요한 패키지를 설치해주세요.")
        sys.exit(1)

def start_server():
    """FastAPI 서버 시작"""
    print("FastAPI 서버를 시작합니다...")
    server_process = subprocess.Popen(
        ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 서버가 시작될 때까지 잠시 대기
    time.sleep(3)
    
    # 서버가 정상적으로 시작되었는지 확인
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("서버 시작에 실패했습니다.")
            server_process.terminate()
            sys.exit(1)
    except requests.RequestException:
        print("서버 시작에 실패했습니다.")
        server_process.terminate()
        sys.exit(1)
    
    print("FastAPI 서버가 정상적으로 시작되었습니다.")
    return server_process

def start_ngrok():
    """ngrok 터널 시작"""
    from pyngrok import ngrok, conf
    
    # ngrok 인증 토큰이 있는 경우 설정
    ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
    if ngrok_token:
        conf.get_default().auth_token = ngrok_token
    
    print("ngrok 터널을 시작합니다...")
    http_tunnel = ngrok.connect(addr="8000")  # 문자열로 포트 전달
    public_url = http_tunnel.public_url
    
    print(f"\n{'='*50}")
    print(f"ngrok 공개 URL: {public_url}")
    print(f"웹훅 URL: {public_url}/webhook")
    print(f"이 URL을 Tally Form의 웹훅 설정에 사용하세요.")
    print(f"{'='*50}\n")
    
    return public_url

def main():
    """메인 실행 함수"""
    print("Tally-Notion 웹훅 서버 시작하기")
    print("=" * 50)
    
    # 필요 패키지 확인
    check_requirements()
    
    # 환경 변수 확인
    if not os.getenv("NOTION_TOKEN") or not os.getenv("NOTION_DATABASE_ID"):
        print("경고: NOTION_TOKEN 또는 NOTION_DATABASE_ID 환경 변수가 설정되어 있지 않습니다.")
        print(".env 파일을 확인해주세요.")
    
    try:
        # FastAPI 서버 시작
        server_process = start_server()
        
        # ngrok 시작
        public_url = start_ngrok()
        
        print("Ctrl+C를 눌러 서버를 종료하세요.")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
    
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
    
    finally:
        # 서버 프로세스 종료
        if 'server_process' in locals():
            server_process.terminate()
            server_process.wait()
        
        # ngrok 터널 종료
        from pyngrok import ngrok
        ngrok.kill()
        
        print("서버가 종료되었습니다.")

if __name__ == "__main__":
    main() 