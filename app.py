from chatbot import ask_taxassist

print("=" * 50)
print("        TaxAssist AI")
print("=" * 50)

while True:

    question = input("\nAsk your tax question (or type 'exit'): ")

    if question.lower() == "exit":
        print("\nThank you for using TaxAssist AI.")
        break

    print("\nThinking...\n")

    answer = ask_taxassist(question)

    print("Answer:")
    print(answer)