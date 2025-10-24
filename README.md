# BankBot: Conversational Banking Assistant

A production-ready banking assistant that uses LangChain and local LLMs (via Ollama) to provide a natural language interface for banking operations.

## Features

- **Natural Language Processing**: Understands commands like "add 100 euros" or "what's my balance?"
- **Banking Operations**:
  - Check account balance
  - Deposit money
  - Withdraw money
  - Currency conversion (EUR to USD)
- **Modular Architecture**: Clean separation of concerns
- **Configurable**: Easy to modify settings and prompts

## Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Ollama** (for local LLM)
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download the model
   ollama pull gemma2:2b
   ```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BrunoMelicio/LLM_Agent_Bank_Assistant.git
   cd LLM_Agent_Bank_Assistant
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

## Quick Start

1. **Start the Ollama server** (in a separate terminal):
   ```bash
   ollama serve
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Example usage**:
   ```
   BankBot: Welcome! How can I assist you today?
   > What's my balance?
   Your current balance is 0.00 EUR
   
   > Deposit 100 euros
   Successfully deposited 100.00 EUR. New balance: 100.00 EUR
   
   > Withdraw 30
   Withdrew 30.00 EUR. New balance: 70.00 EUR
   
   > Convert 50 EUR to USD
   50.00 EUR = 55.00 USD (rate: 1.1)
   
   > exit
   Goodbye! Your final balance is 70.00 EUR
   ```

## Configuration

Configuration is handled through environment variables. Copy the example file and modify as needed:

```bash
cp .env.example .env
```

Key configuration options in `.env`:
- `LLM_PROVIDER`: Choose between 'ollama' or other supported providers
- `LLM_MODEL_NAME`: The LLM model to use (default: 'gemma2:2b')
- `BANKING_CURRENCY`: Base currency (default: 'EUR')
- `BANKING_INITIAL_BALANCE`: Starting balance (default: 0.0)

## Project Structure

```
bankbot/
├── src/
│   └── bankbot/
│       ├── __init__.py
│       ├── app.py            # Main application
│       ├── config/           # Configuration
│       ├── banking/          # Core banking logic
│       ├── llm/              # LLM integration
│       ├── prompts/          # Prompt templates
│       └── utils/            # Helper functions
├── main.py                  # Entry point
├── setup.py                 # Package configuration
└── .env.example             # Example environment variables
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest
```

### Adding New Features

1. **New Banking Operation**:
   - Add method to `BankAccount` class in `banking/account.py`
   - Add handler in `BankBotApp.execute_action()`
   - Update system prompt in `prompts/templates.py`

2. **New LLM Provider**:
   - Add provider logic in `llm/assistant.py`
   - Update configuration in `config/settings.py`

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
