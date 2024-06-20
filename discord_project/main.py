from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, scrape_and_update_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Scheduler setup
scheduler = AsyncIOScheduler()

# Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        logging.info('(Message was empty because intents were not enabled)')
        return

    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        logging.error(e)

# Secure shutdown command
async def shutdown():
    await client.close()

# Startup
@client.event
async def on_ready() -> None:
    logging.info(f'{client.user} is now running!')
    # Schedule the scraping task every morning at 6:20 AM
    scheduler.add_job(scrape_and_update_data, CronTrigger(hour=6, minute=20))
    scheduler.start()
    # Update data.json on startup
    await scrape_and_update_data()

# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message = str(message.content)
    await send_message(message, user_message)

# Run the bot
try:
    client.run(TOKEN)
except Exception as e:
    logging.error(f"Error running bot: {e}")
