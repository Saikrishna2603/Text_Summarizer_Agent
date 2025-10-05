from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.state import *



def add_parts_node(state:state) ->state:
    all_texts=state.get("parts") or []
    new_text=state.get("new_part")
    if new_text is not None and new_text != "":
        state["parts"] = all_texts + [str(new_text)]
        print("Added your text part.\n")
    elif new_text is None or new_text == '':
        print("No new Text Found")
    return state

def summarize_all_node(state:state) ->state:

    parts=state.get("parts") or []
    all_texts = "\n\n".join(parts)
    if not all_texts.strip():
        state["summary"] ="Nothing to Summarize yet . Add parts frist"
        return state

    # Declaring chunk
    chunk_size=state.get("chunk_size") or 2800
    chunk_overlap=state.get("chunk_overlap") or 100
    map_sentences=state.get("map_sentences") or 10
    reduce_sentences=state.get("reduce_sentences") or state.get("sentences") or 6
    style=state.get("style") or "bullet-point"

    # Split the large text to chunks
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=("\n\n","\n","."," ",""),
    )
    chunks=splitter.split_text(all_texts)

    # Now Validate each chunk with the prompts declared int he state.py
    map_chain=MAP_PROMPT | llm
    map_inputs=[{"chunk":c,"style":style,"sentences":map_sentences} for c in chunks]
    map_results =map_chain.batch(map_inputs,max_concurrency=4)
    bullets_summarize=[r.content.strip() for r in map_results]

    if len(bullets_summarize) == 1:
        state["summary"]=bullets_summarize[0]
        return state

    bullets_texts="\n -"+"\n -".join(bullets_summarize)
    reduce_chain=REDUCE_PROMPT | llm
    res=reduce_chain.invoke({
        "bullets": bullets_texts,
        "style":style,
        "sentences":reduce_sentences
    })
    state["summary"] = res.content.strip()
    return state

def router(state: state):
    return "add_part" if state["action"] == "add_part" else "summarize_all"


