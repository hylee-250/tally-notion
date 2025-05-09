import os
from typing import Dict, Any
from notion_client import Client
from datetime import datetime

class NotionClient:
    def __init__(self):
        """Notion API 클라이언트 초기화"""
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.database_id = os.getenv('NOTION_DATABASE_ID')

    def create_page(self, data: Dict[str, Any]) -> bool:
        """Notion 데이터베이스에 새 페이지 생성"""
        try:
            # 데이터베이스 속성 가져오기
            database = self.notion.databases.retrieve(database_id=self.database_id)
            properties = database.get('properties', {})

            # Notion 페이지 데이터 구성
            page_data = {
                "parent": {"database_id": self.database_id},
                "properties": {}
            }

            # 각 필드를 Notion 속성에 매핑
            for key, value in data.items():
                if key in properties:
                    prop_type = properties[key]['type']
                    
                    # 속성 타입에 따라 데이터 형식 변환
                    if prop_type == 'title':
                        page_data['properties'][key] = {
                            'title': [{'text': {'content': str(value)}}]
                        }
                    elif prop_type == 'rich_text':
                        page_data['properties'][key] = {
                            'rich_text': [{'text': {'content': str(value)}}]
                        }
                    elif prop_type == 'number':
                        try:
                            page_data['properties'][key] = {
                                'number': float(value)
                            }
                        except (ValueError, TypeError):
                            continue
                    elif prop_type == 'date':
                        try:
                            date_value = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
                            page_data['properties'][key] = {
                                'date': {
                                    'start': date_value.isoformat()
                                }
                            }
                        except (ValueError, TypeError):
                            continue
                    elif prop_type == 'select':
                        page_data['properties'][key] = {
                            'select': {'name': str(value)}
                        }
                    elif prop_type == 'multi_select':
                        if isinstance(value, list):
                            page_data['properties'][key] = {
                                'multi_select': [{'name': str(v)} for v in value]
                            }
                        else:
                            page_data['properties'][key] = {
                                'multi_select': [{'name': str(value)}]
                            }

            # 페이지 생성
            self.notion.pages.create(**page_data)
            return True

        except Exception as e:
            print(f"Notion 페이지 생성 중 오류 발생: {e}")
            return False

    def get_database_properties(self) -> Dict[str, Any]:
        """데이터베이스 속성 정보 가져오기"""
        try:
            database = self.notion.databases.retrieve(database_id=self.database_id)
            return database.get('properties', {})
        except Exception as e:
            print(f"데이터베이스 속성 가져오기 중 오류 발생: {e}")
            return {}