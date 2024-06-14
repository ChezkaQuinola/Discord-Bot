from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, scrape_and_update_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

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
        print('(Message was empty because intents were not enabled)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Secure shutdown command
async def shutdown():
    await client.close()

# Startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    scheduler.start()

# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message = str(message.content)
    await send_message(message, user_message)

# Schedule the scraping task every morning at 6:20 AM
scheduler.add_job(scrape_and_update_data, CronTrigger(hour=6, minute=20))

# Run the bot
client.run(TOKEN)
