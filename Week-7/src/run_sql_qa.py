from pipelines.sql_pipeline import run_sql_pipeline

print("PRODUCT INVENTORY SQL QA SYSTEM (Groq Powered)")
print("Type 'exit' to quit.\n")

while True:
    question = input("Enter your question: ")

    if question.lower() == "exit":
        break

    try:
        answer = run_sql_pipeline(question)
        print("\nFINAL ANSWER:\n", answer)
        print("\n" + "-" * 50 + "\n")
    except Exception as e:
        print("Error:", e)