import json

def __init_prompt(path):
    with open(path+"prompt_a.json", "r", encoding="utf-8") as f:
        s = f.read()
        print(json.loads(s))    

    with open(path+"prompt_b.json", "r", encoding="utf-8") as f2:
        s = f.read()
        print(json.loads(s)) 

__init_prompt("./")