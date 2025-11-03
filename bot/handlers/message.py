"""Message event handlers."""

import asyncio
import logging
import re
from typing import TYPE_CHECKING, List

import discord

from ..config import config
from ..llm import ConversationMessage, get_service

if TYPE_CHECKING:
    from discord import Client

log = logging.getLogger("bot.handlers.message")


async def build_conversation_history(
    channel: discord.TextChannel | discord.DMChannel | discord.Thread,
    bot_id: int,
    limit: int = 20
) -> List[ConversationMessage]:
    """
    Build conversation history from channel messages.
    
    Args:
        channel: Discord channel to fetch messages from
        bot_id: Bot's user ID
        limit: Number of messages to fetch
    
    Returns:
        List of conversation messages in chronological order
    """
    conversation: List[ConversationMessage] = []
    
    try:
        # Fetch recent messages (most recent first)
        messages = []
        async for msg in channel.history(limit=limit):
            messages.append(msg)
        
        # Reverse to get chronological order (oldest first)
        messages.reverse()
        
        # Convert to conversation format
        for msg in messages:
            # Determine role
            if msg.author.id == bot_id:
                role = "assistant"
            else:
                role = "user"
            
            # Build message content
            content = msg.content or ""
            
            # Add author context for user messages
            if role == "user":
                display_name = msg.author.display_name
                username = msg.author.name
                
                # Check if this is a reply
                reply_info = ""
                if msg.reference and msg.reference.resolved:
                    replied_msg = msg.reference.resolved
                    if hasattr(replied_msg, 'author'):
                        if replied_msg.author.id == bot_id:
                            reply_info = ", replying to you"
                        else:
                            replied_to_name = replied_msg.author.display_name
                            replied_to_username = replied_msg.author.name
                            reply_info = f", replying to {replied_to_name} (@{replied_to_username})"
                
                content = f"[{display_name} (@{username}){reply_info}]: {content}"
            
            # Merge consecutive messages from same role
            if conversation and conversation[-1]["role"] == role:
                conversation[-1]["content"] += "\n" + content
            else:
                conversation.append({"role": role, "content": content})
        
        return conversation
        
    except Exception as e:
        log.exception(f"Error building conversation history: {e}")
        return []


async def generate_and_send_response(
    channel: discord.TextChannel | discord.DMChannel | discord.Thread,
    bot_id: int,
    history: List[discord.Message] = None
) -> None:
    """
    Generate and send a response to the channel.
    
    Args:
        channel: Discord channel to send response to
        bot_id: Bot's user ID
    """
    try:
        # Build conversation history if not provided
        if history is None:
            history = []
            async for msg in channel.history(limit=config.history_limit):
                history.append(msg)
            history.reverse()  # Chronological order
        
        # Build conversation from history
        conversation = []
        for msg in history:
            role = "assistant" if msg.author.id == bot_id else "user"
            content = msg.content or ""
            
            if role == "user":
                display_name = msg.author.display_name
                username = msg.author.name
                reply_info = ""
                
                if msg.reference and msg.reference.resolved:
                    replied_msg = msg.reference.resolved
                    if hasattr(replied_msg, 'author'):
                        if replied_msg.author.id == bot_id:
                            reply_info = ", replying to you"
                        else:
                            replied_to_name = replied_msg.author.display_name
                            replied_to_username = replied_msg.author.name
                            reply_info = f", replying to {replied_to_name} (@{replied_to_username})"
                
                content = f"[{display_name} (@{username}){reply_info}]: {content}"
            
            if conversation and conversation[-1]["role"] == role:
                conversation[-1]["content"] += "\n" + content
            else:
                conversation.append({"role": role, "content": content})
        
        if not conversation:
            log.warning("No conversation history available")
            return
        
        # Log the last user message
        if conversation and conversation[-1]["role"] == "user":
            log.info(f"User message: {conversation[-1]['content'][:100]}...")
        
        # Build environment context
        env_context = {}
        if isinstance(channel, discord.DMChannel):
            env_context["type"] = "DM"
            env_context["dm_with"] = f"{channel.recipient.display_name} (@{channel.recipient.name})"
        else:
            env_context["type"] = "Server"
            if hasattr(channel, "guild") and channel.guild:
                env_context["server_name"] = channel.guild.name
                env_context["member_count"] = channel.guild.member_count
            if hasattr(channel, "name"):
                env_context["channel_name"] = channel.name
            if hasattr(channel, "topic") and channel.topic:
                env_context["channel_description"] = channel.topic
        
        # Generate response
        llm = get_service()
        response = await llm.generate_response(conversation, environment_context=env_context)
        
        if not response:
            log.error("Failed to generate response")
            return
        
        log.info(f"Bot response: {response[:100]}...")
        
        # Split response into multiple messages
        # Split on double newlines first, then single newlines
        if "\n\n" in response:
            parts = response.split("\n\n")
            final_parts = []
            for part in parts:
                if "\n" in part.strip():
                    final_parts.extend(part.split("\n"))
                else:
                    final_parts.append(part)
            parts = final_parts
        else:
            parts = response.split("\n")
        
        # Send each part as a separate message
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            
            # Add delay between messages
            if i > 0:
                delay = 0.5 + (len(part) / 100)
                delay = min(delay, 1.5)
                await asyncio.sleep(delay)
            
            # Check for reply prefix: [reply:username]
            reply_to_message = None
            if part.startswith("[reply:"):
                end_bracket = part.find("]")
                if end_bracket > 0:
                    username = part[7:end_bracket].strip()
                    part = part[end_bracket + 1:].strip()
                    
                    # Find most recent message from this user
                    for msg in reversed(history):
                        if msg.author.name.lower() == username.lower():
                            reply_to_message = msg
                            log.info(f"Replying to @{username}'s message: {msg.id}")
                            break
                    
                    if not reply_to_message:
                        log.warning(f"Could not find message from @{username} to reply to")
            
            # Convert [@username] mentions to Discord mentions
            mention_pattern = r'\[@([^\]]+)\]'
            mentions_found = re.findall(mention_pattern, part)
            
            for username in mentions_found:
                username = username.strip()
                user_id = None
                for msg in history:
                    if msg.author.name.lower() == username.lower():
                        user_id = msg.author.id
                        break
                
                if user_id:
                    part = part.replace(f"[@{username}]", f"<@{user_id}>")
                    log.info(f"Converted [@{username}] to <@{user_id}>")
                else:
                    part = part.replace(f"[@{username}]", f"@{username}")
                    log.warning(f"Could not find user ID for @{username}")
            
            # Show typing indicator and send
            if config.show_typing:
                async with channel.typing():
                    # Brief typing simulation
                    typing_delay = min(len(part) / 100, 2.0)
                    if typing_delay > 0.3:
                        await asyncio.sleep(typing_delay)
                    
                    if reply_to_message:
                        await reply_to_message.reply(part)
                    else:
                        await channel.send(part)
            else:
                if reply_to_message:
                    await reply_to_message.reply(part)
                else:
                    await channel.send(part)
                
    except Exception as e:
        log.exception(f"Error generating and sending response: {e}")


class _null_context:
    """Null context manager for when typing indicator is disabled."""
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        pass


def setup_handlers(client: "Client") -> None:
    """
    Set up message event handlers.
    
    Args:
        client: Discord client instance
    """
    
    @client.event
    async def on_message(message: discord.Message):
        """Handle incoming messages."""
        
        # Ignore our own messages
        if message.author.id == client.user.id:
            return
        
        try:
            bot_id = client.user.id
            should_respond = False
            
            # Trigger 1: Bot is mentioned
            if client.user in message.mentions:
                should_respond = True
                log.info(f"Trigger: Mentioned in {message.channel}")
            
            # Trigger 2: Message is a reply to the bot
            elif message.reference and message.reference.resolved:
                if hasattr(message.reference.resolved, 'author'):
                    if message.reference.resolved.author.id == bot_id:
                        should_respond = True
                        log.info(f"Trigger: Reply to bot in {message.channel}")
            
            # Trigger 3: Message is in a DM
            elif isinstance(message.channel, discord.DMChannel):
                should_respond = True
                log.info(f"Trigger: DM from {message.author}")
            
            # Generate and send response if triggered
            if should_respond:
                await generate_and_send_response(message.channel, bot_id)
                
        except Exception as e:
            log.exception(f"Error in on_message handler: {e}")
