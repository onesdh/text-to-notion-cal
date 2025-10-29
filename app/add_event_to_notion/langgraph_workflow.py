from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .langgraph_nodes import extract_event_node, add_to_notion_node, init_notion_schema_node
from .models import GraphState
from pydantic import BaseModel
from datetime import datetime



def set_graph_state():
    workflow = StateGraph(GraphState)
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompts = {
        "extract_event": f"""
        Today's date is {current_date}.
        Extract event information from the following text.
The output should be a JSON array of EventData objects, adhering to the provided Pydantic schema.
Each EventData object must include a 'title', 'start' (in ISO 8601 format).
'end' (optional, in ISO 8601 format), 'description' (optional), and 'tags' (optional list of strings) should also be extracted if present.
If an end time is not explicitly mentioned but a duration is implied, infer the end time.
If no specific date is mentioned, assume the event is for the nearest future date that makes sense.

Text: {{text}}"""
    
    }
    # 노드 추가
    workflow.add_node("init_notion_schema", init_notion_schema_node())
    workflow.add_node("extract_event", extract_event_node(prompts))
    workflow.add_node("add_to_notion", add_to_notion_node())

    # 엣지 연결
    workflow.add_edge(START, "init_notion_schema")
    workflow.add_edge("init_notion_schema", "extract_event")
    workflow.add_edge("extract_event", "add_to_notion")
    workflow.add_edge("add_to_notion", END)
    app = workflow.compile(checkpointer=MemorySaver())
    return app