from random import choice, randint
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse

# Load the JSON data
with open('parsing_test/data.json', 'r') as file:
    events_data = json.load(file)

def get_response(user_message: str) -> str:
    if user_message.startswith('scrape '):
        url = user_message[7:]
        return scrape_website(url)
    elif user_message.startswith('event on '):
        date_str = user_message[9:]
        return find_event_by_date(date_str)
    else:
        return handle_user_input(user_message)

def scrape_website(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Assuming the response is JSON with a 'rendered' key containing HTML
        data = response.json()
        if 'rendered' in data:
            # Extract the rendered content
            html_content = data['rendered']
            # Remove the rendered key from the JSON data
            del data['rendered']
            # Return the cleaned text
            return html_content
        else:
            return 'No rendered content found in the response.'
    except requests.exceptions.RequestException as e:
        return f'An error occurred: {e}'
    except json.JSONDecodeError:
        return 'Failed to decode JSON from the response.'


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

def find_event_by_date(date_str: str) -> str:
    try:
        # Normalize the user's date input to a consistent format
        query_date = parse(date_str).replace(year=datetime.now().year)
        for event in events_data:
            event_date = datetime.fromisoformat(event['date'])
            if event_date.month == query_date.month and event_date.day == query_date.day:
                title = event.get('title', 'No title found')
                excerpt = event.get('excerpt', 'No excerpt found')
                return f"Title: {title}\nExcerpt: {excerpt}"
        return "No events found for that date."
    except ValueError as e:
        return f"Invalid date format. Please use 'Month day', 'MM/DD', or 'dayth of Month' format."
