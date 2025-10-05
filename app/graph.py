from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START,END
from langgraph.graph import StateGraph
from app.nodes import add_parts_node, summarize_all_node, router
from app.state import state

builder=StateGraph(state)
builder.add_node("add_part", add_parts_node)
builder.add_node("summarize_all",summarize_all_node)

builder.add_conditional_edges(START,router,{
    "add_part":"add_part",
    "summarize_all":"summarize_all",
})
builder.add_edge("add_part",END)
builder.add_edge("summarize_all",END)

#use in memory checkpointer so each thread_id keeps its own parts list
memory=MemorySaver()

#build graph
graph=builder.compile(checkpointer=memory)

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "demo-thread-1"}}

    print("=== Text Summarizer Agent ===")
    print("Type text parts one by one. Type 'summarize' to get summary or 'exit' to quit.")
    while True:
        in_message = input("You: ").strip()
        if in_message.lower() in {"quit", "exit"}:
            break
        elif in_message.lower() == "summarize":
            result = graph.invoke({
                "action": "summarize_all",
                "style": "bullet-point",
                "sentences": 7,
                "map_sentences": 3,
                "chunk_size": 3000,
                "chunk_overlap": 250
            }, config=thread)
            print("\nSummary:\n", result["summary"], "\n")
        else:
            graph.invoke({
                "action": "add_part",
                "new_part": in_message
            }, config=thread)

