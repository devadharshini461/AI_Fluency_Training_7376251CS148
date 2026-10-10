"""Day 6 robust OpenAI-compatible tool-calling agent."""
import os,json,argparse
from dotenv import load_dotenv
from openai import OpenAI
from tools_v2 import TOOLS,execute_tool
load_dotenv();
BASE_URL=os.getenv("OPENAI_BASE_URL","http://localhost:11434/v1");
API_KEY=os.getenv("OPENAI_API_KEY","ollama");
MODEL=os.getenv("MODEL","study-assistant");client=OpenAI(api_key=API_KEY,base_url=BASE_URL)
SYSTEM="""You are a college study helper. Use calculate_percentage for percentage calculations and get_study_tip for study tips. difficulty must be beginner, intermediate or advanced. Do not invent tools or arguments. Answer directly when no tool is needed."""
def run_agent(q,max_steps=6):
    msgs=[{"role":"system","content":SYSTEM},{"role":"user","content":q}];seen={};max_tokens=300;lengths=0
    for step in range(1,max_steps+1):
        try:r=client.chat.completions.create(model=MODEL,messages=msgs,tools=TOOLS,tool_choice="auto",parallel_tool_calls=True,temperature=0,max_tokens=max_tokens)
        except Exception as e:print("API ERROR:",type(e).__name__,e);return
        c=r.choices[0];m=c.message;calls=m.tool_calls or [];print(f"step {step}: finish_reason={c.finish_reason}, tool_calls={len(calls)}")
        if c.finish_reason=="length":
            lengths+=1
            if lengths>=3:print("Stopped: repeated truncation.");return
            max_tokens=min(max_tokens*2,2000);print("Retrying with max_tokens=",max_tokens);continue
        if not calls:print("FINAL:",(m.content or "").strip());return
        msgs.append({"role":"assistant","content":m.content or "","tool_calls":[{"id":x.id,"type":"function","function":{"name":x.function.name,"arguments":x.function.arguments}} for x in calls]})
        if len(calls)>1:print("PARALLEL: multiple calls arrived in one reply")
        for x in calls:
            key=x.function.name+"|"+x.function.arguments;seen[key]=seen.get(key,0)+1
            if seen[key]>3:res="REPEAT_GUARD: identical call repeated more than three times."
            else:
                try:a=json.loads(x.function.arguments or "")
                except json.JSONDecodeError as e:res=f"TOOL_CALL_ERROR: Invalid JSON: {e}"
                else:res=execute_tool(x.function.name,a)
            print(" ",x.function.name,"->",res);msgs.append({"role":"tool","tool_call_id":x.id,"content":str(res)})
    print("MAX_STEP_GUARD: maximum steps reached.")
DEFAULT=["I scored 72 out of 100. What is my percentage?","I scored 72/100 in Python. Give my percentage and a beginner study tip.","Give me an expert-level Python study tip.","What is the difference between a Python list and tuple?"]
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--question");a=ap.parse_args();print("MODEL=",MODEL," BASE_URL=",BASE_URL)
    for i,q in enumerate([a.question] if a.question else DEFAULT,1):print("\n"+"="*70);print("QUESTION",i,":",q);run_agent(q)
