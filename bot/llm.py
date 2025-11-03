"""LLM service for generating responses using Anthropic's Claude API."""

import logging
import os
from typing import Any, Dict, List, Literal, Optional, TypedDict

from anthropic import AsyncAnthropic
from anthropic.types import Message, TextBlock

from .config import config
from .prompt_manager import build_system_prompt

log = logging.getLogger("bot.llm")


class ConversationMessage(TypedDict):
    """Type definition for conversation messages."""
    role: Literal["user", "assistant"]
    content: str


class LLMService:
    """Service for interacting with the Anthropic API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM service.
        
        Args:
            api_key: Anthropic API key (if not provided, reads from env)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. Set it in .env or pass it explicitly."
            )
        
        self.client = AsyncAnthropic(api_key=self.api_key)
    
    async def generate_response(
        self, 
        messages: List[ConversationMessage],
        environment_context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """
        Generate a response using the Claude API.
        
        Args:
            messages: List of conversation messages with role and content
            environment_context: Optional environment context (server, channel, DM info)
            model: Optional model override (uses config default if not provided)
            max_tokens: Optional max tokens override (uses config default if not provided)
        
        Returns:
            Generated response text or None on error
        """
        try:
            # Use config defaults if not provided
            model = model or config.llm_model
            max_tokens = max_tokens or config.max_tokens
            
            # Build system prompt from prompt files with environment context
            system_prompt = build_system_prompt(environment_context)
            
            # Make API request
            response: Message = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages,
            )
            
            # Extract text from response
            text_blocks = [
                block.text for block in response.content 
                if isinstance(block, TextBlock)
            ]
            
            result = "".join(text_blocks) if text_blocks else None
            
            if result:
                log.debug(f"Generated response ({len(result)} chars)")
            
            return result
            
        except Exception as e:
            log.exception(f"Error generating response: {e}")
            return None


# Singleton instance
_service: Optional[LLMService] = None


def get_service() -> LLMService:
    """
    Get the singleton LLM service instance.
    
    Returns:
        LLM service instance
    """
    global _service
    if _service is None:
        _service = LLMService()
    return _service
