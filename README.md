# Tally Form에서 Notion 데이터베이스로 자동 연동하기

이 프로젝트는 Tally Form으로 제출된 데이터를 자동으로 Notion 데이터베이스에 기록하는 웹훅 서버를 제공합니다.

## 기능

- Tally Form 제출 데이터를 Notion 데이터베이스에 자동 기록
- 백그라운드 비동기 처리로 빠른 응답 보장
- 다양한 폼 필드와 Notion 속성 간 매핑 지원
- 실시간 로깅으로 문제 해결 용이
- 건강 체크 엔드포인트 포함

## 설치 및 실행 방법

### 1. 필요 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음과 같이 설정하세요:

```
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
```

### 3. 서버 실행

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

로컬에서 개발 중일 때는 다음 명령어로 실행하여 파일 변경 시 자동으로 서버가 재시작됩니다:

```bash
python app.py
```

## Tally Form 웹훅 설정 방법

1. Tally 대시보드에서 해당 폼의 설정으로 이동
2. 'Integrations' 섹션에서 'Webhooks' 선택
3. 'Add Webhook' 클릭
4. 다음 정보 입력:
   - Webhook URL: `https://your-server.com/webhook` (서버 주소로 변경)
   - Trigger: 'On Form Submit' 선택
   - Payload Format: 'JSON' 선택
5. 'Save' 클릭

## 서버 배포 방법

### ngrok을 사용한 로컬 테스트

로컬에서 개발 중이나 외부에서 접근 가능한 URL이 필요할 때 ngrok을 사용할 수 있습니다:

```bash
ngrok http 8000
```

이 명령어를 실행하면 외부에서 접근 가능한 URL이 생성됩니다. 이 URL을 Tally의 웹훅 URL로 설정하세요.

### 클라우드 서비스에 배포

- Heroku, DigitalOcean, AWS 등의 클라우드 서비스에 배포할 수 있습니다.
- Gunicorn이나 다른 WSGI/ASGI 서버를 사용하여 프로덕션 환경에서 실행하는 것을 권장합니다.

## JSON 파일 처리하기

이전에 구현한 JSON 파일 처리 기능도 여전히 사용 가능합니다:

```bash
python process_json.py response/your_json_file.json
```

## 문제 해결

- 로그 파일 `tally_webhook.log`를 확인하여 오류 정보를 확인하세요.
- `/health` 엔드포인트에 GET 요청을 보내 서버 상태를 확인할 수 있습니다.

## 라이선스

MIT
