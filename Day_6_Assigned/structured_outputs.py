"""Day 6: same extraction question, three response formats."""
import os,json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv();client=OpenAI(api_key=os.getenv("OPENAI_API_KEY","ollama"),base_url=os.getenv("OPENAI_BASE_URL","http://localhost:11434/v1"));MODEL=os.getenv("MODEL","study-assistant")
Q="Extract the student's name, course and score from: 'Anu scored 82 in Python programming.'"
S={"type":"object","properties":{"name":{"type":"string"},"course":{"type":"string"},"score":{"type":"number"}},"required":["name","course","score"],"additionalProperties":False}
def ask(fmt,label):
    print("\n---",label,"---")
    try:
        r=client.chat.completions.create(model=MODEL,messages=[{"role":"system","content":"Extract the requested fields."},{"role":"user","content":Q}],temperature=0,response_format=fmt);raw=(r.choices[0].message.content or "").strip();print("raw:",raw)
        try:print("parsed:",json.loads(raw))
        except Exception as e:print("parsed/error:",e)
    except Exception as e:print("not supported here:",type(e).__name__,e)
if __name__=="__main__":ask(None,"1. no constraint");ask({"type":"json_object"},"2. JSON mode");ask({"type":"json_schema","json_schema":{"name":"student_result","schema":S,"strict":True}},"3. schema mode")
