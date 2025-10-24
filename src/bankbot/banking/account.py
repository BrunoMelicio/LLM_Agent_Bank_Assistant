"""Banking account operations."""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Transaction:
    """Represents a banking transaction."""
    
    action: str
    amount: float
    balance_before: float
    balance_after: float
    success: bool
    message: str


class BankAccount:
    """Manages banking account operations."""
    
    def __init__(self, initial_balance: float = 0.0, currency: str = "EUR"):
        """
        Initialize a bank account.
        
        Args:
            initial_balance: Starting balance
            currency: Account currency
        """
        self._balance = initial_balance
        self._currency = currency
        self._transaction_history = []
    
    @property
    def balance(self) -> float:
        """Get current balance."""
        return self._balance
    
    @property
    def currency(self) -> str:
        """Get account currency."""
        return self._currency
    
    @property
    def transaction_history(self) -> list:
        """Get transaction history."""
        return self._transaction_history.copy()
    
    def deposit(self, amount: float) -> Transaction:
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            Transaction object with result
        """
        if amount <= 0:
            return Transaction(
                action="deposit",
                amount=amount,
                balance_before=self._balance,
                balance_after=self._balance,
                success=False,
                message="Amount must be positive"
            )
        
        balance_before = self._balance
        self._balance += amount
        
        transaction = Transaction(
            action="deposit",
            amount=amount,
            balance_before=balance_before,
            balance_after=self._balance,
            success=True,
            message=f"Deposited {amount:.2f} {self._currency}"
        )
        
        self._transaction_history.append(transaction)
        return transaction
    
    def withdraw(self, amount: float) -> Transaction:
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            Transaction object with result
        """
        if amount <= 0:
            return Transaction(
                action="withdraw",
                amount=amount,
                balance_before=self._balance,
                balance_after=self._balance,
                success=False,
                message="Amount must be positive"
            )
        
        if amount > self._balance:
            return Transaction(
                action="withdraw",
                amount=amount,
                balance_before=self._balance,
                balance_after=self._balance,
                success=False,
                message=f"Insufficient funds. Available: {self._balance:.2f} {self._currency}"
            )
        
        balance_before = self._balance
        self._balance -= amount
        
        transaction = Transaction(
            action="withdraw",
            amount=amount,
            balance_before=balance_before,
            balance_after=self._balance,
            success=True,
            message=f"Withdrew {amount:.2f} {self._currency}"
        )
        
        self._transaction_history.append(transaction)
        return transaction
    
    def get_balance(self) -> float:
        """Get current balance."""
        return self._balance
    
    def convert_currency(self, amount: float, to_currency: str, exchange_rate: float) -> dict:
        """
        Convert currency amount.
        
        Args:
            amount: Amount to convert
            to_currency: Target currency
            exchange_rate: Exchange rate
            
        Returns:
            Dictionary with conversion details
        """
        converted_amount = amount * exchange_rate
        return {
            "from_amount": amount,
            "from_currency": self._currency,
            "to_amount": converted_amount,
            "to_currency": to_currency,
            "exchange_rate": exchange_rate
        }
