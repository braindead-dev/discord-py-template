"""Command handlers for the Discord bot.

Commands are triggered by slash commands registered with Discord.
Add new commands by decorating functions with @command decorator.
"""

import logging
from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from discord import Client

log = logging.getLogger("bot.handlers.commands")


class CommandTree(app_commands.CommandTree):
    """Custom command tree for the bot."""
    
    def __init__(self, client: "Client"):
        super().__init__(client)
    
    async def sync_commands(self, guild: discord.Object = None):
        """Sync commands to Discord."""
        try:
            if guild:
                synced = await self.sync(guild=guild)
                log.info(f"Synced {len(synced)} commands to guild {guild.id}")
            else:
                synced = await self.sync()
                log.info(f"Synced {len(synced)} commands globally")
        except Exception as e:
            log.exception(f"Failed to sync commands: {e}")


def setup_commands(client: "Client", tree: CommandTree) -> None:
    """
    Register all bot commands.
    
    Args:
        client: Discord client instance
        tree: Command tree for registering commands
    """
    
    @tree.command(name="ping", description="Check if the bot is responsive")
    async def ping_command(interaction: discord.Interaction):
        """Simple ping command to test bot responsiveness."""
        log.info(f"Ping command used by {interaction.user}")
        await interaction.response.send_message("pong", ephemeral=True)
    
    # Add more commands here following the same pattern:
    # 
    # @tree.command(name="command_name", description="Command description")
    # async def command_function(interaction: discord.Interaction):
    #     """Command implementation."""
    #     await interaction.response.send_message("Response", ephemeral=True)
    #
    # For commands with parameters:
    # @tree.command(name="echo", description="Echo a message")
    # @app_commands.describe(message="The message to echo")
    # async def echo_command(interaction: discord.Interaction, message: str):
    #     await interaction.response.send_message(message)
    
    log.info("Command handlers registered")
