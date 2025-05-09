# Tally-Google Sheets-Notion Integration

이 프로젝트는 Tally Form 제출 데이터가 Google Spreadsheet에 저장된 후, 이를 Notion 데이터베이스와 연동하는 자동화 시스템입니다.

## 기능

- Google Spreadsheet의 Tally Form 응답 데이터를 주기적으로 확인
- 새로운 응답이 있을 경우 자동으로 Notion 데이터베이스에 동기화
- 중복 데이터 처리 및 에러 핸들링

## 사전 요구사항

1. Python 3.8 이상
2. Tally Form 계정 (무료 버전 사용 가능)
3. Google Cloud Platform 계정 및 프로젝트
4. Notion API 키
5. 필요한 Python 패키지 (requirements.txt에 명시)

## 설치 방법

1. 저장소 클론

```bash
git clone [repository-url]
cd tally-notion
```

2. 가상환경 생성 및 활성화

```bash
conda activate tally
```

3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

## 설정 방법

### 1. Tally Form 설정

1. Tally Form에서 새로운 폼 생성
2. Google Sheets 연동 설정:
   - Tally Form의 'Integrations' 섹션에서 'Google Sheets' 선택
   - Google 계정으로 로그인
   - 새로운 스프레드시트 생성 또는 기존 스프레드시트 선택
   - 응답이 자동으로 스프레드시트에 저장되도록 설정

### 2. Google Sheets API 설정

1. Google Cloud Console에서 프로젝트 생성
2. Google Sheets API 활성화
3. 서비스 계정 생성 및 키 다운로드
4. 다운로드한 키 파일을 프로젝트 루트 디렉토리에 `credentials.json`으로 저장
5. Tally Form이 데이터를 저장하는 스프레드시트에 서비스 계정 이메일 공유 설정
   - 스프레드시트 공유 설정에서 서비스 계정 이메일 추가 (편집자 권한)

### 3. Notion API 설정

1. Notion 통합(integration) 생성
2. API 키 발급
3. Notion 데이터베이스 생성 및 통합 연결
4. 환경 변수 설정:

```bash
export NOTION_API_KEY="your-notion-api-key"
export NOTION_DATABASE_ID="your-database-id"
export GOOGLE_SHEET_ID="your-google-sheet-id"
```

## 실행 방법

1. 메인 애플리케이션 실행

```bash
python app.py
```

## 프로젝트 구조

```
tally-notion/
├── app.py                 # 메인 애플리케이션
├── google_sheets.py       # Google Sheets API 클라이언트
├── notion_client.py       # Notion API 클라이언트
├── process_data.py        # 데이터 처리 로직
├── utils.py              # 유틸리티 함수
├── models.py             # 데이터 모델
└── requirements.txt      # 프로젝트 의존성
```

## 데이터 흐름

1. Tally Form 제출 → Google Spreadsheet 자동 저장
2. 주기적으로 Google Spreadsheet 확인
3. 새로운 데이터 발견 시 → Notion 데이터베이스 동기화

## 문제 해결

1. Google Sheets API 오류

   - credentials.json 파일이 올바른 위치에 있는지 확인
   - 서비스 계정 권한 확인
   - 스프레드시트 ID가 올바른지 확인

2. Notion API 오류
   - API 키가 올바른지 확인
   - 데이터베이스 ID가 올바른지 확인
   - 통합이 데이터베이스에 연결되어 있는지 확인

## 보안 고려사항

1. API 키와 인증 정보는 환경 변수로 관리
2. 서비스 계정 키 파일은 .gitignore에 포함
3. 스프레드시트 접근 권한 관리

## 기여 방법

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 라이선스

MIT License
