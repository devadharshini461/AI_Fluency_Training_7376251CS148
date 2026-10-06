"""Day 6: Study Helper tools, schemas, validation and execution."""
TOPIC_TIPS={"java":{"beginner":"Start with variables, conditions, loops, methods and arrays.","intermediate":"Practice OOP, inheritance, interfaces and exception handling.","advanced":"Practice collections, generics, streams and JVM concepts."},"python":{"beginner":"Start with variables, conditions, loops, functions and lists.","intermediate":"Practice dictionaries, modules, exceptions and file handling.","advanced":"Practice decorators, generators, async programming and advanced libraries."},"sql":{"beginner":"Start with SELECT, WHERE, ORDER BY and basic filtering.","intermediate":"Practice JOIN, GROUP BY, HAVING and subqueries.","advanced":"Practice window functions, CTEs, query optimization and indexing."}}
def calculate_percentage(score:float,total:float)->str:
    try:
        score,total=float(score),float(total)
        if total<=0:return "Error: total must be greater than 0."
        return f"{(score/total)*100:.2f}%"
    except Exception as e:return f"Calculation error: {e}"
def get_study_tip(topic:str,difficulty:str)->str:
    topic=str(topic).strip().lower()
    if topic not in TOPIC_TIPS:return f"Unknown topic: {topic}. Valid topics: {', '.join(TOPIC_TIPS)}"
    return TOPIC_TIPS[topic].get(difficulty,f"Unknown difficulty: {difficulty}")
TOOL_FUNCTIONS={"calculate_percentage":calculate_percentage,"get_study_tip":get_study_tip}
SCHEMAS={"calculate_percentage":{"type":"object","properties":{"score":{"type":"number","description":"Marks obtained."},"total":{"type":"number","description":"Maximum marks."}},"required":["score","total"],"additionalProperties":False},"get_study_tip":{"type":"object","properties":{"topic":{"type":"string","description":"Programming topic."},"difficulty":{"type":"string","enum":["beginner","intermediate","advanced"],"description":"Difficulty level."}},"required":["topic","difficulty"],"additionalProperties":False}}
TOOLS=[{"type":"function","function":{"name":"calculate_percentage","description":"Calculate a student's percentage from obtained and total marks.","parameters":SCHEMAS["calculate_percentage"]}},{"type":"function","function":{"name":"get_study_tip","description":"Give a study tip for a programming topic at a specified difficulty.","parameters":SCHEMAS["get_study_tip"]}}]
def validate_args(tool_name,args):
    if tool_name not in SCHEMAS:return f"Unknown tool: {tool_name}"
    if not isinstance(args,dict):return "Arguments must be a JSON object."
    s=SCHEMAS[tool_name];p=s["properties"]
    for k in s["required"]:
        if k not in args:return f"Missing required argument: '{k}'. Expected: {', '.join(s['required'])}"
    for k in args:
        if k not in p:return f"Unexpected argument: '{k}'. Allowed: {', '.join(p)}"
    for k,v in args.items():
        t=p[k]["type"]
        if t=="string" and not isinstance(v,str):return f"Wrong type for '{k}': expected string, got {type(v).__name__}."
        if t=="number" and (not isinstance(v,(int,float)) or isinstance(v,bool)):return f"Wrong type for '{k}': expected number, got {type(v).__name__}."
        if "enum" in p[k] and v not in p[k]["enum"]:return f"Invalid value for '{k}': {v}. Allowed: {', '.join(p[k]['enum'])}"
    return None
def execute_tool(name,args):
    err=validate_args(name,args)
    if err:return f"VALIDATION_ERROR: {err}"
    try:return str(TOOL_FUNCTIONS[name](**args))
    except Exception as e:return f"TOOL_EXECUTION_ERROR: {e}"
if __name__=="__main__":
    cases=[("valid","calculate_percentage",{"score":80,"total":100}),("missing","calculate_percentage",{"score":80}),("wrong type","calculate_percentage",{"score":"eighty","total":100}),("enum","get_study_tip",{"topic":"java","difficulty":"expert"}),("extra","get_study_tip",{"topic":"java","difficulty":"beginner","extra":"x"})]
    for label,n,a in cases:print(f"{label}: {validate_args(n,a) or execute_tool(n,a)}")
