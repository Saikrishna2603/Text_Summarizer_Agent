from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START,END
from langgraph.graph import StateGraph
from IPython.display import Image,display

from app.nodes import add_parts_node, summarize_all_node, router
from state import *

builder=StateGraph(state)
builder.add_node("add_parts",add_parts_node)
builder.add_node("summarize_all_node",summarize_all_node)

builder.add_conditional_edges(START,router,{
    "add_parts":"add_parts",
    "summarize_all_node":"summarize_all_node",
})
builder.add_edge("add_parts",END)
builder.add_edge("summarize_all_node",END)

#use in memory checkpointer so each thread_id keeps its own parts list
memory=MemorySaver()

#build graph
graph=builder.compile(checkpointer=memory)

display((Image(graph.get_graph().draw_mermaid_png())))

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
                "action": "summarize_all_node",
                "style": "bullet-point",
                "sentences": 5
            }, config=thread)
            print("\n🧠 Summary:\n", result["summary"], "\n")
        else:
            graph.invoke({
                "action": "add_parts",
                "new_parts": in_message
            }, config=thread)
            print("(✓) Added your text part.\n")