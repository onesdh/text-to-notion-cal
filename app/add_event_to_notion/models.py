from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime



class EventData(BaseModel):
    title: str = Field(..., description="이벤트 제목")
    start: datetime = Field(..., description="시작 날짜 및 시간 (ISO 8601 형식)")
    end: Optional[datetime] = Field(None, description="종료 날짜 및 시간 (선택)")
    description: Optional[str] = Field(None, description="이벤트 설명 또는 메모")
    # tags: Optional[List[str]] = Field(None, description="이벤트 관련 태그")

class ExtractEventOutput(BaseModel):
    events: List[EventData] = Field(..., description="추출된 이벤트 리스트")

class LLMConfig(BaseModel):
    model_id: str = Field(..., description="LLM 모델 ID")
    temperature: float = Field(..., description="LLM 온도 설정")
    top_p: float = Field(..., description="LLM Top-p 설정")

class NotionConfig(BaseModel):
    notion_token: Optional[str] = Field(None, description="Notion 통합 토큰")
    notion_database_id: Optional[str] = Field(None, description="Notion 데이터베이스 ID")


class GraphState(BaseModel):
    llm_config: LLMConfig = Field(..., description="LLM 실행 구성")
    notion_config: NotionConfig = Field(..., description="Notion 실행 구성")

    text: str = Field(..., description="사용자 입력 텍스트")
    events: Optional[List[EventData]] = Field(None, description="추출된 이벤트 리스트")
    notion_payloads: Optional[List[dict]] = Field(None, description="Notion API 페이로드 리스트")