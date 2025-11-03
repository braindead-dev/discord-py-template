"""Configuration settings for the Discord bot."""

from dataclasses import dataclass


@dataclass
class BotConfig:
    """Main bot configuration."""
    
    # LLM Model Configuration
    # Available models: claude-sonnet-4-5, claude-opus-4, claude-haiku-4-5
    llm_model: str = "claude-sonnet-4-5"
    
    # Maximum tokens for LLM responses
    max_tokens: int = 2000
    
    # System prompt for the bot's personality and behavior
    system_prompt: str = """You are a helpful and friendly Discord bot assistant.

Your responses should be:
- Conversational and natural
- Helpful and informative
- Concise but complete
- Appropriate for Discord's chat format

You can see the conversation history and should maintain context.
When asked about your capabilities, explain that you respond to mentions and replies.
"""
    
    # Message history limit for context
    # Number of recent messages to include in conversation history
    history_limit: int = 20
    
    # Whether to show typing indicator while generating response
    show_typing: bool = True
    
    # Timeout for typing indicator (seconds)
    typing_timeout: float = 30.0


# Global config instance
config = BotConfig()
