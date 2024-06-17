import html
import schedule
import time
import json
import re
import aiohttp
from datetime import datetime, timedelta
from dateutil.parser import parse
from bs4 import BeautifulSoup
from random import choice, randint


# URL to scrape
DATA_URL = "https://sites.allegheny.edu/my/wp-json/wp/v2/posts"

# Async function to scrape the website and update data.json
async def scrape_and_update_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(DATA_URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            if response.status == 200:
                posts = await response.json()
                events_data = []

                for post in posts:
                    title = html.unescape(post['title']['rendered'])

                    # Extract the excerpt from the 'entry' class in the HTML content
                    soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
                    excerpt = soup.get_text() if soup else 'No excerpt found'
                    excerpt = html.unescape(excerpt)

                    events_data.append({
                        'title': title,
                        'excerpt': excerpt
                    })

                with open('data.json', 'w') as file:
                    json.dump(events_data, file, indent=2)
            else:
                print(f"Failed to fetch data. Status code: {response.status}")

# Load the JSON data initially
with open('parsing_test/data.json', 'r') as file:
    events_data = json.load(file)

def get_response(user_message: str) -> str:
    if any(keyword in user_message.lower() for keyword in ["event on", "any events on", "anything happening on", "happening on"]):
        date_str = user_message.split("on")[-1].strip()
        return find_events_by_date(date_str)
    elif "any events today" in user_message.lower():
        today_date_str = datetime.now().strftime("%B %d")
        return find_events_by_date(today_date_str)
    else:
        return handle_user_input(user_message)

def handle_user_input(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return "Hello there! :)"
    elif 'how are you' in lowered:
        return "Good, thanks!"
    elif 'bye' in lowered:
        return "See you later!"
    elif 'roll dice' in lowered:
        return f"You rolled: {randint(1, 6)}"
    else:
        return choice([
            "I do not understand...",
            "What are you talking about?",
            "Do you mind rephrasing that?"
        ])

def find_events_by_date(date_str: str) -> str:
    try:
        # Normalize the user's date input to a consistent format
        query_date = parse(date_str).replace(year=datetime.now().year)
        events_found = []

        for event in events_data:
            title = event['title']
            excerpt = event['excerpt']
            
            event_dates = extract_dates_from_text(title + " " + excerpt)
            
            if any(query_date.date() in date_range for date_range in event_dates):
                events_found.append(f"Title: {title}\nExcerpt: {excerpt}")

        if events_found:
            # Join the events with a line separator
            return "\n\n---\n\n".join(events_found)
        else:
            return "No events found for that date."
    except ValueError as e:
        return f"Invalid date format. Please use 'Month day', 'MM/DD', or 'dayth of Month' format."

def extract_dates_from_text(text: str):
    """
    Extracts dates from the given text. This function handles different date formats and ranges.
    Returns a list of date ranges (as sets of dates).
    """
    date_patterns = [
        r'\b(\d{1,2}/\d{1,2})\b',           # Matches MM/DD or M/D
        r'\b(\w+ \d{1,2})\b',                # Matches Month DD or Month D
        r'\b(\d{1,2}-\d{1,2})\b',            # Matches M-D or MM-DD
        r'\b(\d{1,2}/\d{1,2}-\d{1,2})\b',    # Matches MM/DD-DD or M/D-D
        r'\b(\w+ \d{1,2}-\d{1,2})\b'         # Matches Month DD-DD or Month D-D
    ]

    date_ranges = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                if '-' in match:
                    # Handle date ranges
                    if '/' in match:
                        start_date_str, end_date_str = match.split('/')[-1].split('-')
                        start_date = parse(match.split('-')[0]).replace(year=datetime.now().year).date()
                        end_date = parse(end_date_str).replace(year=datetime.now().year).date()
                    else:
                        start_date_str, end_date_str = match.split('-')
                        start_date = parse(start_date_str).replace(year=datetime.now().year).date()
                        end_date = parse(end_date_str).replace(year=datetime.now().year).date()
                    date_ranges.append(set([start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]))
                else:
                    # Handle single dates
                    date = parse(match).replace(year=datetime.now().year).date()
                    date_ranges.append(set([date]))
            except ValueError:
                continue
    return date_ranges

