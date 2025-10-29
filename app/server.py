# server.py
import logging
from mcp.server.fastmcp import FastMCP
from add_event_to_notion.langgraph_workflow import set_graph_state
from add_event_to_notion.models import GraphState, LLMConfig, NotionConfig
from config import GPT_LLM_MODEL, TEMPERATURE, TOP_P, NOTION_TOKEN, NOTION_DATABASE_ID

# ✅ 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ✅ MCP 서버 인스턴스 생성
mcp = FastMCP("notion_event_extractor", port = 8001)

@mcp.tool()
def add_event_to_notion(text: str):
    """
    자연어 일정 문장을 받아
    → LangGraph를 통해 일정 추출 후
    → Notion 데이터베이스에 자동 추가합니다.
    """
    logger.info(f"🚀 '{text}'에 대한 Notion 일정 추가 요청을 받았습니다.")
    try:
        # 설정 객체 구성
        llm_config = LLMConfig(
            model_id=GPT_LLM_MODEL,
            temperature=TEMPERATURE,
            top_p=TOP_P
        )
        notion_config = NotionConfig(
            notion_token=NOTION_TOKEN,
            notion_database_id=NOTION_DATABASE_ID
        )

        # 초기 그래프 상태 구성
        initial_state = GraphState(
            text=text,
            llm_config=llm_config,
            notion_config=notion_config
        )

        # LangGraph 실행
        logger.info("🧠 LangGraph 워크플로우를 시작합니다.")
        app = set_graph_state()
        result = app.invoke(initial_state, config={"configurable": {"thread_id": f"ontology_{GPT_LLM_MODEL}"}})
        logger.info("✅ LangGraph 워크플로우가 성공적으로 완료되었습니다.")

        # 결과 정리
        notion_pages = []
        final_payloads = result.get("notion_payloads")
        if final_payloads:
            for p in final_payloads:
                notion_pages.append(p.get("url", "🔗 (URL 없음)"))

        success_message = f"✅ {len(notion_pages)}개의 일정이 Notion에 추가되었습니다.\n" + "\n".join(notion_pages)
        logger.info(success_message)
        return success_message

    except Exception as e:
        logger.error(f"❌ 처리 중 오류가 발생했습니다: {e}", exc_info=True)
        return f"오류가 발생하여 일정을 추가하지 못했습니다. 시스템 로그를 확인해주세요. (오류: {e})"


# ✅ MCP 서버 실행
if __name__ == "__main__":
    mcp.run(transport="sse")