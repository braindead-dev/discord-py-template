"""Centralized prompt management for the Discord bot.

All prompts are stored as .txt files in the prompts/ directory and loaded here.
This ensures consistent prompt management across the application.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """
    Load a prompt from the prompts directory.
    
    Args:
        filename: Name of the prompt file (e.g., "base.txt")
    
    Returns:
        Prompt text, stripped of leading/trailing whitespace
    
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text().strip()


def build_system_prompt(environment_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Compose the full system prompt for conversation responses.
    
    Args:
        environment_context: Optional dict with 'type', 'channel_name', 'server_name', etc.
    
    Returns:
        Complete system prompt for the bot's personality and behavior
    """
    parts = []
    
    # Profile (who the bot is)
    parts.append(load_prompt("profile.txt"))
    
    # Base prompt (communication style, behavior guidelines, etc.)
    parts.append(load_prompt("base.txt"))
    
    # Dynamic environment context
    env_text = build_environment_header(environment_context)
    parts.append(env_text)
    
    return "\n\n".join(parts)


def build_environment_header(environment_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Build dynamic environment context header with current date/time and location.
    
    Args:
        environment_context: Dict with 'type', 'channel_name', 'server_name', etc.
    
    Returns:
        Formatted environment header string
    """
    # Get current time
    now = datetime.now()
    
    # Format: "Sunday, November 3rd, 1:45PM"
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    day = now.day
    
    # Add ordinal suffix (1st, 2nd, 3rd, 4th, etc.)
    if 10 <= day <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    time_str = now.strftime("%I:%M%p").lstrip("0")  # Remove leading zero from hour
    date_str = f"{day_name}, {month_name} {day}{suffix}, {time_str}"
    
    # Determine location
    if environment_context and environment_context.get("type") == "DM":
        location = "in a DM"
    elif environment_context and environment_context.get("channel_name"):
        channel_name = environment_context.get("channel_name")
        location = f"in #{channel_name}"
        if environment_context.get("server_name"):
            location += f" on {environment_context.get('server_name')}"
    else:
        location = "in Discord"
    
    return (
        f"# Current Context\n"
        f"It's {date_str}. This conversation is happening {location}."
    )
