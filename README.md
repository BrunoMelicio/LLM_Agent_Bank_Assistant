# 🏦 LLM Agent Bank Assistant

A conversational banking application powered by a local LLM (Large Language Model) using Ollama. Interact with your bank account using natural language instead of traditional menu-driven interfaces!

## 📋 Overview

This project demonstrates how to build an intelligent banking assistant that understands natural language commands. Instead of selecting numbered menu options, you can simply tell the assistant what you want to do in plain English.

**Example interactions:**
- "What's my balance?"
- "Add 100 euros to my account"
- "I want to withdraw 50"
- "Convert 25 EUR to USD"

## ✨ Features

- **💰 Check Balance** - View your current account balance in EUR
- **➕ Deposit Money** - Add funds to your account
- **➖ Withdraw Money** - Withdraw funds (with insufficient balance protection)
- **💱 Currency Conversion** - Convert EUR to USD
- **🤖 Natural Language Interface** - Powered by Ollama's local LLM (Gemma2:2b)

## 🎯 Goal

The goal of this project is to showcase how LLMs can be integrated into simple applications to create more intuitive and conversational user experiences. By using a locally-running LLM via Ollama, the application maintains privacy while providing intelligent command interpretation.

## 🛠️ Prerequisites

Before running this application, you need to have the following installed:

### 1. Python 3.7+
Check if Python is installed:
```bash
python3 --version
```

### 2. Ollama
Ollama is required to run the local LLM model.

**Installation:**
- **macOS/Linux:**
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Windows:** Download from [ollama.com](https://ollama.com)

**Verify installation:**
```bash
ollama --version
```

### 3. Gemma2:2b Model
Pull the required model:
```bash
ollama pull gemma2:2b
```

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BrunoMelicio/LLM_Agent_Bank_Assistant.git
   cd LLM_Agent_Bank_Assistant
   ```

2. **Install Python dependencies:**
   ```bash
   pip install ollama
   ```

## 🚀 Usage

### Step 1: Start Ollama Server
In a separate terminal window, start the Ollama service:
```bash
ollama serve
```

Keep this terminal running while using the application.

### Step 2: Run the Bank Assistant
In your main terminal, run:
```bash
python main.py
```

### Step 3: Interact with the Assistant
Once the application starts, you can type natural language commands:

```
🏦 Local Bank Assistant (Ollama LLM)
Type 'exit' to quit.

You: What's my balance?
🧩 LLM → {'action': 'check_balance'}
💰 Balance: 0.00 EUR

You: Add 100 euros
🧩 LLM → {'action': 'add', 'amount': 100}
✅ Added 100.00 EUR → New balance: 100.00 EUR

You: Withdraw 30
🧩 LLM → {'action': 'withdraw', 'amount': 30}
✅ Withdrew 30.00 EUR → New balance: 70.00 EUR

You: Convert 50 EUR to dollars
🧩 LLM → {'action': 'convert_usd', 'amount': 50}
💱 50.00 EUR = 55.00 USD

You: exit
👋 Bye! Final balance: 70.00 EUR
```

## 🔧 Configuration

You can modify the following settings in `main.py`:

- **`MODEL`** (line 6): Change the LLM model (default: `gemma2:2b`)
- **`EUR_TO_USD`** (line 5): Update the exchange rate
- **`balance`** (line 4): Set initial balance (default: 0.0)

## 🧠 How It Works

1. **User Input**: You type a natural language command
2. **LLM Processing**: The command is sent to the local Ollama LLM
3. **Intent Recognition**: The LLM interprets your intent and returns structured JSON
4. **Action Execution**: The application executes the corresponding banking operation
5. **Feedback**: Results are displayed to the user

## 🐛 Troubleshooting

### "Could not connect to Ollama" error
- Make sure Ollama is running: `ollama serve`
- Check if the model is installed: `ollama list`
- Verify Ollama is accessible: `ollama run gemma2:2b "Hello"`

### LLM returns unexpected responses
- The model might need clearer prompts
- Try rephrasing your command
- Check that the model is properly loaded

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 👤 Author

**Bruno Melicio**
- GitHub: [@BrunoMelicio](https://github.com/BrunoMelicio)

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) for providing an easy way to run LLMs locally
- [Google Gemma](https://ai.google.dev/gemma) for the Gemma2 model
