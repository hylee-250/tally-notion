import requests
import json
import sys

def send_test_data(url, endpoint="/zapier"):
    """
    테스트 데이터를 지정된 URL로 전송합니다.
    """
    full_url = f"{url.rstrip('/')}{endpoint}"
    
    # 테스트용 데이터
    test_data = {
        "이름": "테스트 사용자",
        "날짜": "Apr 10, 2025",
        "시간": "12:30",
        "연락처": "010-1234-5678",
        "학년": "고등학교 1학년",
        "입학_테스트_희망_시간": None
    }
    
    print(f"\n{full_url}로 테스트 데이터를 전송합니다...")
    
    try:
        response = requests.post(full_url, json=test_data, timeout=10)
        print(f"응답 상태 코드: {response.status_code}")
        
        try:
            print(f"응답 내용: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"응답 내용: {response.text}")
            
        return response
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python send_test_data.py <URL> [엔드포인트]")
        print("예시: python send_test_data.py https://example.ngrok.io /zapier")
        sys.exit(1)
    
    url = sys.argv[1]
    endpoint = sys.argv[2] if len(sys.argv) > 2 else "/zapier"
    
    send_test_data(url, endpoint) 