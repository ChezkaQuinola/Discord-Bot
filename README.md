# Discord Bot

## Overview

This Discord bot retrieves and displays information about events from a specified website using the Wordpress API. It provides users with event details based on specific queries related to dates and general inquiries.

## Features

- **Event Query**: Responds to queries about events happening on specific dates or today.
- **Interactive Responses**: Provides formatted responses with Markdown and hyperlinks.
- **Automatic Updates**: Automatically scrapes and updates event data daily at 6:20 AM.
- **Error Handling**: Handles invalid date formats and unexpected user inputs gracefully.

## Installation

1. **Clone Repository:**
   ```
   git clone git@github.com:ChezkaQuinola/Discord-Bot.git
   cd Discord-Bot
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Create a `.env` file in the root directory with the following:
   ```
   DISCORD_TOKEN=<your-discord-bot-token>
   ```

4. **Run the Bot:**
   ```
   python discord_project/main.py
   ```

5. **Interact with the Bot:**
   - Join the Discord server where the bot is deployed.
   - Type commands to query events, such as:
     - `event on June 21`
     - `any events today`
     - `roll dice`

## Dependencies

- `discord.py`: Python library for building Discord bots.
- `requests`: HTTP library for making requests.
- `aiohttp`: Asynchronous HTTP client/server framework for asyncio.
- `beautifulsoup4`: Library for parsing HTML and XML documents.
- `python-dotenv`: Library for loading environment variables from a `.env` file.

## Usage

- **Commands:**
  - `event on <date>`: Retrieves events happening on a specific date.
  - `any events today`: Retrieves events happening today.
  - `roll dice`: Rolls a six-sided dice.
  - Other general interactions like greetings and farewells.

## Contributors

- [Chezka Quinola](https://github.com/ChezkaQuinola)
