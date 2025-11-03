# Discord.py Bot Template

A production-ready Discord bot template with LLM integration using Anthropic's Claude API.

## Features

- 🤖 **Modern discord.py architecture** - Clean separation of concerns with handlers
- 🧠 **LLM Integration** - Anthropic Claude API for intelligent responses
- 🎯 **Smart Triggers** - Responds to @mentions, replies, and DMs
- ⚡ **Slash Commands** - Modern slash command system with `/ping` example
- 💬 **Multiple Messages** - Automatically splits on newlines for natural conversation flow
- 🔁 **Reply Feature** - Bot can reply to specific messages using `[reply:username]` syntax
- 📢 **Mentions** - Bot can @mention users using `[@username]` syntax
- ⏱️ **Typing Indicators** - Shows realistic typing behavior
- 📁 **Prompt Management** - Organized prompts in separate .txt files
- ⚙️ **Easy Configuration** - Centralized config system
- 📝 **Logging** - Comprehensive logging setup
- 🔒 **Environment Variables** - Secure credential management

## Project Structure

```
discord-py-template/
├── bot/                    # Main bot package
│   ├── __init__.py        # Package initialization
│   ├── client.py          # Discord client setup
│   ├── config.py          # Bot configuration
│   ├── llm.py             # LLM service integration
│   ├── prompt_manager.py  # Prompt loading and management
│   ├── prompts/           # Prompt text files
│   │   ├── profile.txt    # Bot personality/identity
│   │   └── base.txt       # Communication guidelines
│   └── handlers/          # Event handlers
│       ├── __init__.py
│       ├── message.py     # Message event handler
│       └── commands.py    # Slash command handler
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Setup

### 1. Prerequisites

- Python 3.10 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Anthropic API Key ([Get one here](https://console.anthropic.com/))

### 2. Installation

```bash
# Clone or download this template
cd discord-py-template

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your tokens
# DISCORD_TOKEN=your_bot_token_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Running the Bot

```bash
python main.py
```

## Usage

The bot will respond to:
- **Direct mentions** - `@BotName hello there`
- **Replies** - Reply to any of the bot's messages
- **DMs** - All messages in DMs
- **Slash commands** - `/ping` to check if bot is responsive

### Bot Capabilities

The bot has several special features:

#### Multiple Messages
The bot can send multiple separate Discord messages by using double newlines in its response:
```
Message 1

Message 2

Message 3
```

#### Reply to Specific Messages
The bot can reply to a specific user's message using:
```
[reply:username] your response here
```

#### Mention Users
The bot can @mention users using:
```
[@username] your message
```

### Configuration

Edit `bot/config.py` to customize:
- **LLM Model** - Change the Claude model (default: `claude-sonnet-4-5`)
- **Max Tokens** - Adjust response length limits
- **Message History** - Change how many messages to include in context
- **Typing Indicators** - Enable/disable typing simulation

Edit `bot/prompts/` to customize:
- **profile.txt** - Bot's personality and identity
- **base.txt** - Communication guidelines and behavior rules

## Development

### Adding New Commands

To add a new slash command, edit `bot/handlers/commands.py`:

```python
@tree.command(name="hello", description="Say hello")
async def hello_command(interaction: discord.Interaction):
    """Greet the user."""
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

# Command with parameters
@tree.command(name="echo", description="Echo a message")
@app_commands.describe(message="The message to echo")
async def echo_command(interaction: discord.Interaction, message: str):
    """Echo back the user's message."""
    await interaction.response.send_message(message)
```

Commands will automatically sync to Discord when the bot starts.

### Adding New Message Handlers

Create new handler modules in `bot/handlers/` and register them in `bot/client.py`:

```python
from .handlers import message, your_new_handler

message.setup_handlers(client)
your_new_handler.setup_handlers(client)
```

### Customizing LLM Behavior

Modify `bot/llm.py` to:
- Add tool/function calling
- Change prompt templates
- Add conversation history management
- Implement caching or optimization

## Troubleshooting

### Bot doesn't respond
- Check that the bot has the correct permissions in your Discord server
- Ensure the bot has the "Message Content Intent" enabled in the Discord Developer Portal
- Verify your tokens are correct in `.env`

### LLM errors
- Check your Anthropic API key is valid
- Ensure you have credits in your Anthropic account
- Check the logs for specific error messages

## License

MIT License - Feel free to use this template for any project!
