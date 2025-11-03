# Discord.py Bot Template

A production-ready Discord bot template with LLM integration using Anthropic's Claude API.

## Features

- 🤖 **Modern discord.py architecture** - Clean separation of concerns with handlers
- 🧠 **LLM Integration** - Anthropic Claude API for intelligent responses
- 🎯 **Smart Triggers** - Responds to @mentions and replies
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
│   └── handlers/          # Event handlers
│       ├── __init__.py
│       └── message.py     # Message event handler
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

### Configuration

Edit `bot/config.py` to customize:
- **LLM Model** - Change the Claude model (default: `claude-sonnet-4-5`)
- **Max Tokens** - Adjust response length limits
- **System Prompt** - Customize bot personality and behavior

## Development

### Adding New Handlers

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
