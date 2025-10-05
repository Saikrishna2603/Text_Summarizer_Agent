from app.graph import graph

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
            print("Added your text part.\n")
