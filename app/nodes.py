from state import *



def add_parts_node(state:state) ->state:
    all_texts=state.get("parts") or []
    new_text=state.get("new_parts")
    state["parts"]=all_texts+[new_text]
    return state

def summarize_all_node(state:state) ->state:

    parts=state.get("parts") or []
    all_texts = "\n\n".join(parts)
    if not all_texts.strip():
        state["summary"] ="Nothing to Summarize yet . Add parts frist"
        return state
    chain =sum_prompt | llm
    #Checking the
    res=chain.invoke({
        "all_text": all_texts,
        "style":state.get("style") or "Concise ParaGraph",
        "sentence":state.get("sentence") or 6
    })
    state["summary"] = res.content
    return state

def router(state:state):
    return "add_parts" if state["action"] == "add_parts" else "summarize_all_node"


