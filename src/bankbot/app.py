"""Main application controller for BankBot."""

from typing import Optional

from .config.settings import llm_config, banking_config, app_config
from .banking.account import BankAccount
from .llm.assistant import BankingAssistant
from .prompts.templates import PromptTemplates
from .utils.parser import ResponseParser


class BankBotApp:
    """Main application controller."""
    
    def __init__(self):
        """Initialize the BankBot application."""
        self.account = BankAccount(
            initial_balance=banking_config.initial_balance,
            currency=banking_config.currency
        )
        self.assistant = BankingAssistant(
            config=llm_config,
            max_history=banking_config.max_history_messages
        )
        self.parser = ResponseParser()
        self.templates = PromptTemplates()
        self.action_messages = self.templates.get_action_messages()
        self.error_messages = self.templates.get_error_messages()
    
    def execute_action(self, action_dict: dict) -> bool:
        """
        Execute a banking action.
        
        Args:
            action_dict: Dictionary containing action and parameters
            
        Returns:
            True if action was executed, False otherwise
        """
        if not self.parser.validate_action(action_dict):
            return False
        
        action = action_dict.get("action")
        amount = action_dict.get("amount", 0)
        
        if action == "check_balance":
            print(f"\n{self.action_messages['balance_check'].format(balance=self.account.balance, currency=self.account.currency)}")
            return True
        
        elif action == "add":
            transaction = self.account.deposit(amount)
            if transaction.success:
                print(f"\n{self.action_messages['deposit'].format(amount=amount, balance=self.account.balance, currency=self.account.currency)}")
            else:
                print(f"\n{transaction.message}")
            return transaction.success
        
        elif action == "withdraw":
            transaction = self.account.withdraw(amount)
            if transaction.success:
                print(f"\n{self.action_messages['withdraw'].format(amount=amount, balance=self.account.balance, currency=self.account.currency)}")
            else:
                print(f"\n{self.error_messages['insufficient_funds'].format(balance=self.account.balance, currency=self.account.currency)}")
            return transaction.success
        
        elif action == "convert_usd":
            conversion = self.account.convert_currency(
                amount=amount,
                to_currency="USD",
                exchange_rate=banking_config.eur_to_usd_rate
            )
            print(f"\n{self.action_messages['convert'].format(amount=amount, from_currency=conversion['from_currency'], converted=conversion['to_amount'], to_currency=conversion['to_currency'])}")
            return True
        
        return False
    
    def process_user_input(self, user_input: str) -> bool:
        """
        Process user input through the LLM and execute actions.
        
        Args:
            user_input: User's message
            
        Returns:
            True if processing was successful, False otherwise
        """
        # Get LLM response
        reply = self.assistant.chat(
            user_input=user_input,
            current_balance=self.account.balance,
            currency=self.account.currency
        )
        
        if reply is None:
            return False
        
        # Parse response
        conversational_text, action_dict = self.parser.parse_response(reply)
        
        # Print conversational response
        if conversational_text:
            print(f"\nBankBot: {conversational_text}")
        
        # Execute action if present
        if action_dict:
            self.execute_action(action_dict)
        
        return True
    
    def run(self):
        """Run the main application loop."""
        # Print welcome message
        print(self.templates.get_welcome_message())
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                    print(self.templates.get_goodbye_message(
                        balance=self.account.balance,
                        currency=self.account.currency
                    ))
                    break
                
                # Process input
                self.process_user_input(user_input)
            
            except KeyboardInterrupt:
                print(self.templates.get_goodbye_message(
                    balance=self.account.balance,
                    currency=self.account.currency
                ))
                break
            except Exception as e:
                if app_config.debug:
                    print(f"\n⚠️ Unexpected error: {e}")
                else:
                    print(f"\n{self.error_messages['parse_error']}")
