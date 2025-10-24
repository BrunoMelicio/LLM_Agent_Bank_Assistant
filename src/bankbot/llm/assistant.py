"""LLM-powered banking assistant."""

from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

from ..config.settings import LLMConfig
from ..prompts.templates import PromptTemplates


class BankingAssistant:
    """LangChain-powered conversational banking assistant."""
    
    def __init__(self, config: LLMConfig, max_history: int = 10):
        """
        Initialize the banking assistant.
        
        Args:
            config: LLM configuration
            max_history: Maximum number of messages to keep in history
        """
        self.config = config
        self.max_history = max_history
        
        # Initialize LLM based on provider
        self.llm = self._initialize_llm()
        
        # Initialize chat message history
        self.chat_history = ChatMessageHistory()
        
        # Create prompt template
        self.prompt = None
        self.chain = None
    
    def _initialize_llm(self):
        """Initialize the LLM based on configuration."""
        if self.config.provider.lower() == "ollama":
            return ChatOllama(
                model=self.config.model_name,
                temperature=self.config.temperature,
                base_url=self.config.base_url if self.config.base_url else None
            )
        # Add other providers here (OpenAI, Anthropic, etc.)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.provider}")
    
    def _create_prompt_template(self, system_prompt: str) -> ChatPromptTemplate:
        """
        Create a prompt template with the given system prompt.
        
        Args:
            system_prompt: System prompt text
            
        Returns:
            ChatPromptTemplate instance
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
    
    def update_system_prompt(self, balance: float, currency: str = "EUR"):
        """
        Update the system prompt with current balance.
        
        Args:
            balance: Current account balance
            currency: Currency code
        """
        system_prompt = PromptTemplates.get_system_prompt(balance, currency)
        self.prompt = self._create_prompt_template(system_prompt)
        self.chain = self.prompt | self.llm
    
    def chat(self, user_input: str, current_balance: float, currency: str = "EUR") -> Optional[str]:
        """
        Send a message and get a response.
        
        Args:
            user_input: User's message
            current_balance: Current account balance
            currency: Currency code
            
        Returns:
            Assistant's response or None if error
        """
        try:
            # Update system prompt with current balance
            self.update_system_prompt(current_balance, currency)
            
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
            if len(self.chat_history.messages) > self.max_history:
                self.chat_history.messages = self.chat_history.messages[-self.max_history:]
            
            return response.content
        
        except Exception as e:
            error_messages = PromptTemplates.get_error_messages()
            print(error_messages["llm_connection"].format(error=str(e)))
            return None
    
    def clear_history(self):
        """Clear the chat history."""
        self.chat_history.clear()
    
    def get_history_length(self) -> int:
        """Get the number of messages in history."""
        return len(self.chat_history.messages)
