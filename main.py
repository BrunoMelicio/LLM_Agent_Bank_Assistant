"""
BankBot - A Conversational Banking Assistant

Entry point for the BankBot application.
"""

from src.bankbot.app import BankBotApp


def main():
    """Main entry point for the application."""
    app = BankBotApp()
    app.run()


if __name__ == "__main__":
    main()
