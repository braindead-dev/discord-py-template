"""Discord client setup and initialization."""

import logging
import os
from typing import Optional

import discord
from dotenv import load_dotenv

from .config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger("bot")


def create_client() -> discord.Client:
    """
    Create and configure the Discord client.
    
    Returns:
        Configured Discord client with intents and handlers
    """
    # Configure intents
    intents = discord.Intents.default()
    intents.message_content = True  # Required to read message content
    intents.members = True  # Optional: for member-related features
    
    # Create client
    client = discord.Client(intents=intents)
    
    # Register event handlers
    from .handlers import message
    message.setup_handlers(client)
    
    # Ready event
    @client.event
    async def on_ready():
        log.info(
            f"Bot logged in as {client.user.name} (ID: {client.user.id})"
        )
        log.info(f"Connected to {len(client.guilds)} server(s)")
    
    return client


def run_bot(token: Optional[str] = None) -> None:
    """
    Run the Discord bot.
    
    Args:
        token: Discord bot token (if not provided, reads from env)
    """
    # Load environment variables
    load_dotenv()
    
    # Get token
    if not token:
        token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        raise SystemExit(
            "DISCORD_TOKEN is not set. Create a .env file or export it in your shell."
        )
    
    # Create and run client
    client = create_client()
    
    try:
        client.run(token)
    except KeyboardInterrupt:
        log.info("Bot stopped by user")
    except Exception as e:
        log.exception(f"Error running bot: {e}")
        raise
