def main():
    balance = 0.0
    EUR_TO_USD = 1.10  # Exchange rate (approximate)
    
    while True:
        print("\n" + "="*40)
        print("BANK ASSISTANT")
        print("="*40)
        print("1. Check balance")
        print("2. Withdraw money")
        print("3. Add money")
        print("4. Convert to USD")
        print("5. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            # Check balance
            print(f"\nCurrent balance: {balance:.2f} EUR")
        
        elif choice == "2":
            # Withdraw money
            try:
                amount = float(input("Enter amount to withdraw (EUR): "))
                if amount <= 0:
                    print("Error: Amount must be positive!")
                elif amount > balance:
                    print(f"Error: Insufficient funds! Available balance: {balance:.2f} EUR")
                else:
                    balance -= amount
                    print(f"Successfully withdrew {amount:.2f} EUR")
                    print(f"New balance: {balance:.2f} EUR")
            except ValueError:
                print("Error: Invalid amount entered!")
        
        elif choice == "3":
            # Add money
            try:
                amount = float(input("Enter amount to add (EUR): "))
                if amount <= 0:
                    print("Error: Amount must be a positive number!")
                elif amount != int(amount):
                    print("Error: Only positive integers are allowed!")
                else:
                    balance += amount
                    print(f"Successfully added {amount:.0f} EUR")
                    print(f"New balance: {balance:.2f} EUR")
            except ValueError:
                print("Error: Invalid amount entered!")
        
        elif choice == "4":
            # Convert to USD
            try:
                amount = float(input("Enter amount in EUR to convert to USD: "))
                if amount <= 0:
                    print("Error: Amount must be positive!")
                else:
                    usd_amount = amount * EUR_TO_USD
                    print(f"{amount:.2f} EUR = {usd_amount:.2f} USD")
            except ValueError:
                print("Error: Invalid amount entered!")
        
        elif choice == "5":
            # Exit
            print("\nThank you for using Bank Assistant!")
            print(f"Final balance: {balance:.2f} EUR")
            break
        
        else:
            print("Error: Invalid choice! Please select 1-5.")


if __name__ == "__main__":
    main()
