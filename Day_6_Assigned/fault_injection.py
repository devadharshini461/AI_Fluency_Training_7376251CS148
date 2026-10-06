"""Day 6 fault injection. No model or internet is required."""
import json
from tools_v2 import TOOL_FUNCTIONS,execute_tool
FAULTS=[("invalid JSON","calculate_percentage",'{"score":80,"total":100'),("unknown tool","send_email",'{"to":"x"}'),("missing required","calculate_percentage",'{"score":80}'),("wrong type","calculate_percentage",'{"score":"eighty","total":100}'),("enum violation","get_study_tip",'{"topic":"python","difficulty":"expert"}'),("invented argument","get_study_tip",'{"topic":"python","difficulty":"beginner","extra":"x"}'),("negative total (custom)","calculate_percentage",'{"score":80,"total":-100}'),("unknown topic (custom)","get_study_tip",'{"topic":"rust","difficulty":"beginner"}')]
def handle(tool,raw):
    try:a=json.loads(raw)
    except json.JSONDecodeError as e:return f"Argument error: invalid JSON ({e})"
    if tool not in TOOL_FUNCTIONS:return f"Unknown tool: {tool}. Available tools: {', '.join(TOOL_FUNCTIONS)}"
    return execute_tool(tool,a)
if __name__=="__main__":
    for label,tool,raw in FAULTS:print(f"{label:<32} -> {handle(tool,raw)} | run continued: Y")
