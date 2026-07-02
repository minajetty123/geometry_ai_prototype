"""
chat.py
CLI chat loop for the geometry agent.
The agent can create, resize, and erase shapes (in pixels),
and also answer questions about the geometry component using RAG.

Usage:
    python chat.py
"""

from agent import build_agent


def main():
    print("=" * 55)
    print("  Geometry Agent (Qwen2.5-Coder + Tools)")
    print("  Type 'exit' to quit.")
    print("=" * 55)
    print("Examples:")
    print("  'Create a circle with radius 50px'")
    print("  'Make it bigger by 20px'")
    print("  'Create a rectangle 100x60px'")
    print("  'Erase circle_1'")
    print("  'List all shapes'")
    print("  'Why does Circle throw an error with radius -1?'")
    print("=" * 55)

    try:
        agent = build_agent()
    except Exception as e:
        print(f"\n[ERROR] Could not initialise: {e}")
        print("Make sure:\n  1. pip install -r requirements.txt\n  2. python index_code.py")
        return

    print("\nReady!\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Bye!")
            break

        try:
            result = agent.run(question)
            print(f"\nAssistant: {result}\n")
        except Exception as e:
            print(f"\n[ERROR] {e}\n")


if __name__ == "__main__":
    main()

