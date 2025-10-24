"""Configuration settings for BankBot."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class LLMConfig(BaseSettings):
    """LLM configuration settings."""
    
    provider: str = Field(default="ollama", description="LLM provider (ollama, openai, etc.)")
    model_name: str = Field(default="gemma2:2b", description="Model name to use")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    base_url: Optional[str] = Field(default=None, description="Base URL for API")
    api_key: Optional[str] = Field(default=None, description="API key if required")
    
    class Config:
        env_prefix = "LLM_"
        env_file = ".env"
        env_file_encoding = "utf-8"


class BankingConfig(BaseSettings):
    """Banking configuration settings."""
    
    initial_balance: float = Field(default=0.0, description="Initial account balance")
    currency: str = Field(default="EUR", description="Base currency")
    eur_to_usd_rate: float = Field(default=1.1, description="EUR to USD exchange rate")
    max_history_messages: int = Field(default=10, description="Maximum chat history messages")
    
    class Config:
        env_prefix = "BANKING_"
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppConfig(BaseSettings):
    """Application configuration."""
    
    app_name: str = Field(default="BankBot", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global configuration instances
llm_config = LLMConfig()
banking_config = BankingConfig()
app_config = AppConfig()
