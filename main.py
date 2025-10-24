from ollama import chat
import json
import re

balance = 0.0
EUR_TO_USD = 1.1
MODEL = "gemma2:2b"
conversation_history = []


def ask_llm(user_message: str, current_balance: float):
    """Ask the LLM for a conversational response and detect banking actions."""
    system_prompt = f"""
You are a friendly banking assistant named BankBot. You can have natural conversations with users while helping them manage their bank account.

Current account balance: {current_balance:.2f} EUR

When the user wants to perform a banking action, include a JSON object in your response using this EXACT format:
{{"action": "ACTION_NAME", "amount": NUMBER}}

Available actions:
- check_balance: Check account balance (no amount needed, use 0)
- add: Deposit money to account
- withdraw: Withdraw money from account  
- convert_usd: Convert EUR to USD

IMPORTANT: 
- Always respond conversationally first
- If a banking action is requested, include the JSON in your response
- For greetings, small talk, or questions, just respond naturally without JSON
- Be friendly, helpful, and professional

Examples:
- User: "Hi!" → "Hello! I'm BankBot, your banking assistant. How can I help you today?"
- User: "Add 100 euros" → "Sure! I'll add 100 EUR to your account. {{"action": "add", "amount": 100}}"
- User: "How are you?" → "I'm doing great, thank you for asking! How can I assist you with your banking needs today?"
"""
    
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Build messages with system prompt and history
    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    
    try:
        response = chat(model=MODEL, messages=messages)
        assistant_reply = response.message.content.strip()
        
        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # Keep conversation history manageable (last 10 messages)
        if len(conversation_history) > 10:
            conversation_history.pop(0)
            conversation_history.pop(0)
        
        return assistant_reply
    except Exception as e:
        print("⚠️ Could not connect to Ollama:", e)
        print("👉 Make sure 'ollama serve' is running in another terminal.")
        return None

def extract_and_execute_action(response_text: str):
    """Extract JSON action from response and execute it."""
    global balance
    
    # Try to find JSON in the response
    json_match = re.search(r'\{[^}]+\}', response_text)
    
    if json_match:
        try:
            json_str = json_match.group(0)
            parsed = json.loads(json_str)
            action = parsed.get("action")
            amount = parsed.get("amount", 0)
            
            if action == "check_balance":
                print(f"\n💰 Current Balance: {balance:.2f} EUR")
            elif action == "add":
                balance += amount
                print(f"\n✅ Deposited {amount:.2f} EUR → New balance: {balance:.2f} EUR")
            elif action == "withdraw":
                if amount > balance:
                    print(f"\n❌ Insufficient funds! Available: {balance:.2f} EUR")
                else:
                    balance -= amount
                    print(f"\n✅ Withdrew {amount:.2f} EUR → New balance: {balance:.2f} EUR")
            elif action == "convert_usd":
                usd = amount * EUR_TO_USD
                print(f"\n💱 {amount:.2f} EUR = {usd:.2f} USD")
            
            return True
        except json.JSONDecodeError:
            return False
    
    return False
        
def main():
    print("🏦 BankBot - Your Conversational Banking Assistant")
    print("💬 Chat naturally with me! I can help with deposits, withdrawals, balance checks, and currency conversion.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print(f"\nBankBot: Goodbye! It was nice talking to you. Your final balance is {balance:.2f} EUR. Have a great day! 👋")
            break
        
        # Get LLM response
        reply = ask_llm(user_input, balance)
        
        if reply is None:
            continue
        
        # Extract conversational part (remove JSON if present)
        conversational_reply = re.sub(r'\{[^}]+\}', '', reply).strip()
        
        # Print the conversational response
        if conversational_reply:
            print(f"\nBankBot: {conversational_reply}")
        
        # Execute any banking action found in the response
        extract_and_execute_action(reply)

if __name__ == "__main__":
    main()