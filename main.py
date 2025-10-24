from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import json
import re

# Configuration
balance = 0.0
EUR_TO_USD = 1.1
MODEL = "gemma2:2b"


class BankingAssistant:
    """LangChain-powered conversational banking assistant."""
    
    def __init__(self, model_name: str):
        # Initialize Ollama LLM
        self.llm = ChatOllama(model=model_name, temperature=0.7)
        
        # Initialize chat message history (keeps last 10 messages = 5 exchanges)
        self.chat_history = ChatMessageHistory()
        self.max_messages = 10  # Keep last 10 messages
        
        # Create prompt template with system message and chat history
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Create the chain
        self.chain = self.prompt | self.llm
    
    def _get_system_prompt(self) -> str:
        """Return the system prompt for the banking assistant."""
        return """You are a friendly banking assistant named BankBot. You can have natural conversations with users while helping them manage their bank account.

                Current account balance: {balance:.2f} EUR

                When the user wants to perform a banking action, include a JSON object in your response using this EXACT format:
                {{{{"action": "ACTION_NAME", "amount": NUMBER}}}}

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
                - Remember the user's name if they tell you

                Examples:
                - User: "Hi!" → "Hello! I'm BankBot, your banking assistant. How can I help you today?"
                - User: "Add 100 euros" → "Sure! I'll add 100 EUR to your account. {{{{"action": "add", "amount": 100}}}}"
                - User: "How are you?" → "I'm doing great, thank you for asking! How can I assist you with your banking needs today?"
                """
    
    def update_balance(self, new_balance: float):
        """Update the system prompt with new balance."""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt().format(balance=new_balance)),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        self.chain = self.prompt | self.llm
    
    def chat(self, user_input: str, current_balance: float) -> str:
        """Send a message and get a response."""
        try:
            # Update balance in system prompt
            self.update_balance(current_balance)
            
            # Get current chat history messages
            messages = self.chat_history.messages
            
            # Invoke the chain
            response = self.chain.invoke({
                "input": user_input,
                "chat_history": messages
            })
            
            # Add messages to history
            self.chat_history.add_user_message(user_input)
            self.chat_history.add_ai_message(response.content)
            
            # Keep only last N messages (window)
            if len(self.chat_history.messages) > self.max_messages:
                # Remove oldest messages (keep last max_messages)
                self.chat_history.messages = self.chat_history.messages[-self.max_messages:]
            
            return response.content
        
        except Exception as e:
            print(f"⚠️ Error communicating with LLM: {e}")
            print("👉 Make sure 'ollama serve' is running in another terminal.")
            return None


def extract_and_execute_action(response_text: str, current_balance: float) -> float:
    """Extract JSON action from response and execute it. Returns updated balance."""
    
    # Try to find JSON in the response
    json_match = re.search(r'\{[^}]+\}', response_text)
    
    if json_match:
        try:
            json_str = json_match.group(0)
            parsed = json.loads(json_str)
            action = parsed.get("action")
            amount = parsed.get("amount", 0)
            
            if action == "check_balance":
                print(f"\n💰 Current Balance: {current_balance:.2f} EUR")
                return current_balance
            
            elif action == "add":
                new_balance = current_balance + amount
                print(f"\n✅ Deposited {amount:.2f} EUR → New balance: {new_balance:.2f} EUR")
                return new_balance
            
            elif action == "withdraw":
                if amount > current_balance:
                    print(f"\n❌ Insufficient funds! Available: {current_balance:.2f} EUR")
                    return current_balance
                else:
                    new_balance = current_balance - amount
                    print(f"\n✅ Withdrew {amount:.2f} EUR → New balance: {new_balance:.2f} EUR")
                    return new_balance
            
            elif action == "convert_usd":
                usd = amount * EUR_TO_USD
                print(f"\n💱 {amount:.2f} EUR = {usd:.2f} USD")
                return current_balance
            
        except json.JSONDecodeError:
            pass
    
    return current_balance


def main():
    """Main application loop."""
    global balance
    
    print("🏦 BankBot - Your Conversational Banking Assistant (LangChain Edition)")
    print("💬 Chat naturally with me! I can help with deposits, withdrawals, balance checks, and currency conversion.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    # Initialize the assistant
    assistant = BankingAssistant(MODEL)
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print(f"\nBankBot: Goodbye! It was nice talking to you. Your final balance is {balance:.2f} EUR. Have a great day! 👋")
            break
        
        # Get LLM response
        reply = assistant.chat(user_input, balance)
        
        if reply is None:
            continue
        
        # Extract conversational part (remove JSON if present)
        conversational_reply = re.sub(r'\{[^}]+\}', '', reply).strip()
        
        # Print the conversational response
        if conversational_reply:
            print(f"\nBankBot: {conversational_reply}")
        
        # Execute any banking action found in the response and update balance
        balance = extract_and_execute_action(reply, balance)


if __name__ == "__main__":
    main()
