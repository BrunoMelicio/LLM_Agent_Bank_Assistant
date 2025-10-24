"""Prompt templates for BankBot."""

from typing import Dict


class PromptTemplates:
    """Collection of prompt templates for different LLM interactions."""
    
    @staticmethod
    def get_system_prompt(balance: float, currency: str = "EUR") -> str:
        """
        Get the system prompt for the banking assistant.
        
        Args:
            balance: Current account balance
            currency: Currency code (default: EUR)
            
        Returns:
            Formatted system prompt string
        """
        return f"""You are a friendly banking assistant named BankBot. You can have natural conversations with users while helping them manage their bank account.

                    Current account balance: {balance:.2f} {currency}

                    When the user wants to perform a banking action, include a JSON object in your response using this EXACT format:
                    {{{{"action": "ACTION_NAME", "amount": NUMBER}}}}

                    Available actions:
                    - check_balance: Check account balance (no amount needed, use 0)
                    - add: Deposit money to account
                    - withdraw: Withdraw money from account  
                    - convert_usd: Convert {currency} to USD

                    IMPORTANT: 
                    - Always respond conversationally first
                    - If a banking action is requested, include the JSON in your response
                    - For greetings, small talk, or questions, just respond naturally without JSON
                    - Be friendly, helpful, and professional
                    - Remember the user's name if they tell you

                    Examples:
                    - User: "Hi!" → "Hello! I'm BankBot, your banking assistant. How can I help you today?"
                    - User: "Add 100 euros" → "Sure! I'll add 100 {currency} to your account. {{{{"action": "add", "amount": 100}}}}"
                    - User: "How are you?" → "I'm doing great, thank you for asking! How can I assist you with your banking needs today?"
                """

    @staticmethod
    def get_welcome_message() -> str:
        """Get the welcome message for the application."""
        return """🏦 BankBot - Your Conversational Banking Assistant
                💬 Chat naturally with me! I can help with deposits, withdrawals, balance checks, and currency conversion.
                Type 'exit' or 'quit' to end the conversation.
                """

    @staticmethod
    def get_goodbye_message(balance: float, currency: str = "EUR") -> str:
        """
        Get the goodbye message.
        
        Args:
            balance: Final account balance
            currency: Currency code
            
        Returns:
            Formatted goodbye message
        """
        return f"\nBankBot: Goodbye! It was nice talking to you. Your final balance is {balance:.2f} {currency}. Have a great day! 👋"

    @staticmethod
    def get_error_messages() -> Dict[str, str]:
        """Get error message templates."""
        return {
            "llm_connection": "⚠️ Error communicating with LLM: {error}\n👉 Make sure 'ollama serve' is running in another terminal.",
            "insufficient_funds": "❌ Insufficient funds! Available: {balance:.2f} {currency}",
            "invalid_amount": "❌ Invalid amount. Please provide a positive number.",
            "parse_error": "⚠️ Couldn't parse the response. Please try again."
        }

    @staticmethod
    def get_action_messages() -> Dict[str, str]:
        """Get action confirmation message templates."""
        return {
            "balance_check": "💰 Current Balance: {balance:.2f} {currency}",
            "deposit": "✅ Deposited {amount:.2f} {currency} → New balance: {balance:.2f} {currency}",
            "withdraw": "✅ Withdrew {amount:.2f} {currency} → New balance: {balance:.2f} {currency}",
            "convert": "💱 {amount:.2f} {from_currency} = {converted:.2f} {to_currency}"
        }
