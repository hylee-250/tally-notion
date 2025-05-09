import os
from typing import List, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime

class GoogleSheetsClient:
    def __init__(self, credentials_path: str = 'credentials.json'):
        """Google Sheets API 클라이언트 초기화"""
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.credentials_path = credentials_path
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.service = self._get_service()

    def _get_service(self):
        """Google Sheets API 서비스 생성"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=self.SCOPES)
            service = build('sheets', 'v4', credentials=credentials)
            return service
        except Exception as e:
            print(f"Google Sheets API 서비스 생성 중 오류 발생: {e}")
            raise

    def get_sheet_data(self, range_name: str = 'A:Z') -> pd.DataFrame:
        """스프레드시트에서 데이터 가져오기"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                print('데이터가 없습니다.')
                return pd.DataFrame()

            # 첫 번째 행을 컬럼명으로 사용
            headers = values[0]
            data = values[1:]
            
            # 데이터프레임 생성
            df = pd.DataFrame(data, columns=headers)
            return df

        except HttpError as error:
            print(f"Google Sheets API 호출 중 오류 발생: {error}")
            raise

    def get_new_responses(self, last_sync_time: datetime) -> List[Dict[str, Any]]:
        """마지막 동기화 이후의 새로운 응답 가져오기"""
        try:
            df = self.get_sheet_data()
            
            # 타임스탬프 컬럼이 있다고 가정
            if 'Timestamp' in df.columns:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                new_responses = df[df['Timestamp'] > last_sync_time]
                
                return new_responses.to_dict('records')
            else:
                print("Timestamp 컬럼을 찾을 수 없습니다.")
                return []

        except Exception as e:
            print(f"새로운 응답을 가져오는 중 오류 발생: {e}")
            return []

    def get_latest_response_time(self) -> datetime:
        """가장 최근 응답의 타임스탬프 가져오기"""
        try:
            df = self.get_sheet_data()
            
            if 'Timestamp' in df.columns:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                return df['Timestamp'].max()
            else:
                print("Timestamp 컬럼을 찾을 수 없습니다.")
                return datetime.min

        except Exception as e:
            print(f"최신 응답 시간을 가져오는 중 오류 발생: {e}")
            return datetime.min 