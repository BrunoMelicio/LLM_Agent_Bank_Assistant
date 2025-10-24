# BankBot Architecture

## Project Structure

```
BankAssistant/
├── src/
│   └── bankbot/
│       ├── __init__.py
│       ├── app.py                 # Main application controller
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py        # Configuration management
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── templates.py       # Prompt templates
│       ├── banking/
│       │   ├── __init__.py
│       │   └── account.py         # Banking operations
│       ├── llm/
│       │   ├── __init__.py
│       │   └── assistant.py       # LLM integration
│       └── utils/
│           ├── __init__.py
│           └── parser.py          # Response parsing utilities
├── main.py                        # Entry point
├── setup.py                       # Package setup
├── requirements.txt               # Dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # User documentation
├── ARCHITECTURE.md                # This file
└── LICENSE                        # License file
```

## Module Descriptions

### 1. **config/** - Configuration Management
- **settings.py**: Centralized configuration using Pydantic Settings
  - `LLMConfig`: LLM provider settings (model, temperature, API keys)
  - `BankingConfig`: Banking parameters (currency, exchange rates)
  - `AppConfig`: Application settings (debug mode, version)
  - Environment variable support via `.env` file

### 2. **prompts/** - Prompt Engineering
- **templates.py**: All prompt templates in one place
  - System prompts with dynamic balance injection
  - Welcome/goodbye messages
  - Error message templates
  - Action confirmation templates
  - Easy to modify and version control prompts

### 3. **banking/** - Business Logic
- **account.py**: Core banking operations
  - `BankAccount` class: Manages account state
  - `Transaction` dataclass: Represents transactions
  - Methods: deposit(), withdraw(), get_balance(), convert_currency()
  - Transaction history tracking
  - Validation and error handling

### 4. **llm/** - LLM Integration
- **assistant.py**: LangChain-powered assistant
  - `BankingAssistant` class: Handles LLM interactions
  - Provider-agnostic design (supports Ollama, OpenAI, etc.)
  - Chat history management with configurable window
  - Dynamic system prompt updates
  - Error handling and fallbacks

### 5. **utils/** - Utilities
- **parser.py**: Response parsing utilities
  - `ResponseParser` class: Extract JSON and text from responses
  - Regex-based JSON extraction
  - Action validation
  - Separation of conversational text and commands

### 6. **app.py** - Application Controller
- **BankBotApp** class: Orchestrates all components
  - Initializes account, assistant, and utilities
  - Main application loop
  - User input processing
  - Action execution
  - Error handling

## Design Principles

### 1. **Separation of Concerns**
Each module has a single, well-defined responsibility:
- Configuration is separate from logic
- Prompts are separate from code
- Banking logic is independent of LLM
- LLM integration is provider-agnostic

### 2. **Modularity**
- Easy to swap LLM providers
- Easy to modify prompts without touching code
- Easy to extend banking operations
- Easy to add new features

### 3. **Configuration Over Code**
- All settings in environment variables
- No hardcoded values
- Easy deployment to different environments
- Support for multiple LLM providers

### 4. **Type Safety**
- Pydantic models for configuration
- Type hints throughout
- Dataclasses for structured data
- Better IDE support and error catching

### 5. **Testability**
- Each module can be tested independently
- Dependency injection ready
- Mock-friendly design
- Clear interfaces

## Data Flow

```
User Input
    ↓
main.py (Entry Point)
    ↓
BankBotApp.process_user_input()
    ↓
BankingAssistant.chat() → LLM Response
    ↓
ResponseParser.parse_response() → (Text, Action)
    ↓
BankBotApp.execute_action()
    ↓
BankAccount.deposit/withdraw/etc()
    ↓
Output to User
```

## Configuration Flow

```
.env file
    ↓
settings.py (Pydantic Settings)
    ↓
llm_config, banking_config, app_config
    ↓
Used by: BankingAssistant, BankAccount, BankBotApp
```

## Extending the Application

### Adding a New LLM Provider

1. Update `src/bankbot/llm/assistant.py`:
```python
def _initialize_llm(self):
    if self.config.provider.lower() == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            api_key=self.config.api_key
        )
```

2. Update `.env.example`:
```
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key-here
```

### Adding a New Banking Operation

1. Add method to `BankAccount` in `src/bankbot/banking/account.py`
2. Add action handler in `BankBotApp.execute_action()`
3. Update system prompt in `src/bankbot/prompts/templates.py`
4. Add message template if needed

### Modifying Prompts

All prompts are in `src/bankbot/prompts/templates.py`. Simply edit the methods:
- `get_system_prompt()` - Main assistant behavior
- `get_welcome_message()` - Startup message
- `get_goodbye_message()` - Exit message
- `get_error_messages()` - Error templates
- `get_action_messages()` - Action confirmations

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `LLM_PROVIDER`: Which LLM to use (ollama, openai, etc.)
- `LLM_MODEL_NAME`: Specific model name
- `BANKING_CURRENCY`: Base currency
- `DEBUG`: Enable debug output

## Production Considerations

1. **Security**
   - Never commit `.env` file
   - Use environment variables in production
   - Rotate API keys regularly

2. **Performance**
   - Configure `max_history_messages` based on needs
   - Monitor LLM API costs
   - Consider caching for repeated queries

3. **Reliability**
   - Implement retry logic for LLM calls
   - Add logging for debugging
   - Handle network failures gracefully

4. **Scalability**
   - Stateless design allows horizontal scaling
   - Consider database for persistent accounts
   - Add authentication for multi-user support
