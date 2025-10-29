from pydantic import BaseModel
from typing import Optional
from dateutil.parser import parse
from .models import ExtractEventOutput, GraphState, EventData
from langchain_core.prompts import PromptTemplate
from .llm_functions import llm_custom_build

from notion_client import Client
import pytz

def init_notion_schema_node():
    """
    Notion 데이터베이스의 스키마를 검사하고,
    Title, Date, Description 속성이 없으면 자동으로 추가합니다.
    """
    def action(state: GraphState):
        notion = Client(auth=state.notion_config.notion_token)
        print("Notion 데이터베이스 스키마 확인 중...")
        # 데이터베이스 스키마 조회
        db = notion.databases.retrieve(database_id=state.notion_config.notion_database_id)
        props = db.get("properties", {})

        desired_props = {
            "Name": {"title": {}},
            "Date": {"date": {}},
            "Description": {"rich_text": {}}
        }

        # 존재하지 않는 속성만 추가
        missing_props = {
            name: schema for name, schema in desired_props.items()
            if name not in props
        }

        if not missing_props:
            print("모든 필요한 속성이 이미 존재합니다.")
            return state

        # 속성 업데이트
        try:
            print(f"누락된 속성 추가 중: {list(missing_props.keys())}")
            notion.databases.update(
                database_id=state.notion_config.notion_database_id,
                properties=missing_props
            )
            print("Notion 데이터베이스 스키마 업데이트 완료!")
        except Exception as e:
            print(f"스키마 업데이트 실패: {e}")

        return state

    return action

def extract_event_node(prompts):
    def action(state: GraphState):
        text = state.text
        llm_config = state.llm_config

        prompt_template = PromptTemplate(
            text=["text"],
            template=prompts["extract_event"]
        )
        prompt_str = prompt_template.format(text=text)
        llm_custom = llm_custom_build(model_id=llm_config.model_id, temperature=llm_config.temperature, top_p=llm_config.top_p, format_model=ExtractEventOutput.model_json_schema())
        response = llm_custom.invoke(input=prompt_str).content
        parsed = ExtractEventOutput.model_validate_json(response)

        print(f"추출된 이벤트 개수: {len(parsed.events)}")
        state.events = parsed.events
        print(f"{parsed.events}")

        return state

    return action


def create_notion_page(event: EventData, notion_token: str, notion_database_id: str):
    """
    Notion 데이터베이스에 이벤트 추가
    - 입력 datetime은 KST 기준 (tzinfo 없음)
    - Notion 캘린더에서 KST 시각 그대로 표시
    """
    notion = Client(auth=notion_token)

    start_dt = event.start
    end_dt = event.end

    # tzinfo가 있다면 제거 (즉, +09:00 없애기)
    if start_dt.tzinfo is not None:
        start_dt = start_dt.replace(tzinfo=None)
    if end_dt and end_dt.tzinfo is not None:
        end_dt = end_dt.replace(tzinfo=None)

    # Notion 속성 구성
    properties = {
        "Name": {
            "title": [{"text": {"content": event.title}}]
        },
        "Date": {
            "date": {
                "start": start_dt.isoformat(),
                "end": end_dt.isoformat() if end_dt else None,
                "time_zone": "Asia/Seoul"
            }
        }
    }

    if event.description:
        properties["Description"] = {
            "rich_text": [{"text": {"content": event.description}}]
        }

    response = notion.pages.create(
        parent={"database_id": notion_database_id},
        properties=properties
    )

    print(f"Notion 일정 추가 완료: {event.title}")
    print(f"저장된 시간 (KST 그대로): {start_dt} ~ {end_dt}")
    return response

def add_to_notion_node():
    def action(state: GraphState):
        if not state.events:
            return state

        results = []
        for event in state.events:
            res = create_notion_page(event, state.notion_config.notion_token, state.notion_config.notion_database_id)
            results.append(res)
        state.notion_payloads = results
        return state

    return action