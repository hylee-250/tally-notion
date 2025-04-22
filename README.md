# Tally-Notion 연동 서비스

Tally 폼 제출 데이터를 Notion 데이터베이스에 자동으로 기록해주는 서비스입니다.

## 설치 방법

1. 필요한 패키지 설치하기:

```bash
pip install -r requirements.txt
```

2. 환경 변수 설정하기:
   `.env` 파일을 생성하고 다음 정보를 추가합니다:

```
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
```

## 로컬에서 테스트하기

로컬 환경에서 테스트하려면 다음 명령어를 실행합니다:

```bash
uvicorn main:app --reload  # FastAPI 실행
ngrok http 8000
```

실행하면:

ngrok 서버 URL
https://922f-14-52-23-180.ngrok-free.app

1. 로컬 FastAPI 서버가 시작됩니다.
2. ngrok을 통해 인터넷에 공개 URL이 생성됩니다.

## 서버 배포하기

FastAPI 앱을 Heroku, Render, Railway 등의 서비스에 배포할 수 있습니다.

```bash
# 예: Heroku로 배포하기
heroku create
git push heroku main
```

배포된 URL을 Zapier의 Webhook URL로 사용하면 됩니다.
