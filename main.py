from ollama import chat
import json

balance = 0.0
EUR_TO_USD = 1.1
MODEL = "gemma2:2b"


def ask_llm(user_message: str):
    """Ask the LLM to interpret the user's intent as JSON."""
    prompt = f"""
        You are a banking assistant. 
        Decide which action the user wants to take and reply ONLY as JSON like:
        {{"action": "add", "amount": 50}}
        Possible actions: add, withdraw, check_balance, convert_usd.

        User: {user_message}
        Assistant:
    """
    try:
        response = chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
        return response.message.content.strip()
    except Exception as e:
        print("⚠️ Could not connect to Ollama:", e)
        print("👉 Make sure 'ollama serve' is running in another terminal.")
        return None

def handle_action(parsed):
    """Execute the action returned by the LLM."""
    global balance
    action = parsed.get("action")
    amount = parsed.get("amount", 0)

    if action == "check_balance":
        print(f"💰 Balance: {balance:.2f} EUR")
    elif action == "add":
        balance += amount
        print(f"✅ Added {amount:.2f} EUR → New balance: {balance:.2f} EUR")
    elif action == "withdraw":
        if amount > balance:
            print(f"❌ Not enough funds (Balance: {balance:.2f} EUR)")
        else:
            balance -= amount
            print(f"✅ Withdrew {amount:.2f} EUR → New balance: {balance:.2f} EUR")
    elif action == "convert_usd":
        usd = amount * EUR_TO_USD
        print(f"💱 {amount:.2f} EUR = {usd:.2f} USD")
    else:
        print("🤖 Sorry, I didn’t understand that.")
        
def main():
    print("🏦 Local Bank Assistant (Ollama LLM)\nType 'exit' to quit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print(f"👋 Bye! Final balance: {balance:.2f} EUR")
            break
        try:
            reply = ask_llm(user_input)
            json_data = json.loads(reply[reply.index("{"): reply.rindex("}")+1])
            print("🧩 LLM →", json_data)
            handle_action(json_data)
        except Exception:
            print("⚠️ Couldn't parse model reply:", reply)

if __name__ == "__main__":
    main()