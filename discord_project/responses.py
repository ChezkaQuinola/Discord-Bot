import html
import requests
import json
from datetime import datetime
from dateutil.parser import parse

# URL to scrape
DATA_URL = "https://sites.allegheny.edu/my/wp-json/wp/v2/posts"

# Function to scrape the website and update data.json
def scrape_and_update_data():
    response = requests.get(DATA_URL, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        with open('data.json', 'w') as file:
            json.dump(response.json(), file, indent=2)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# Load the JSON data initially
with open('data.json', 'r') as file:
    events_data = json.load(file)

def get_response(user_message: str) -> str:
    if any(keyword in user_message.lower() for keyword in ["event on", "any events on", "anything happening on", "happening on"]):
        date_str = user_message.split("on")[-1].strip()
        return find_events_by_date(date_str)
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
            title = html.unescape(event['title']['rendered'])
            excerpt = html.unescape(event['excerpt']['rendered'])
            
            event_dates = extract_dates_from_text(title + " " + excerpt)
            
            if any(query_date.date() in date_range for date_range in event_dates):
                events_found.append(f"Title: {title}\nExcerpt: {excerpt}")

        if events_found:
            return "\n\n".join(events_found)
        else:
            return "No events found for that date."
    except ValueError as e:
        return f"Invalid date format. Please use 'Month day', 'MM/DD', or 'dayth of Month' format."

def extract_dates_from_text(text: str):
    """
    Extracts dates from the given text. This function handles different date formats and ranges.
    Returns a list of date ranges (as sets of dates).
    """
    date_ranges = []
    for word in text.split():
        try:
            if '-' in word:
                start_date_str, end_date_str = word.split('-')
                start_date = parse(start_date_str).replace(year=datetime.now().year).date()
                end_date = parse(end_date_str).replace(year=datetime.now().year).date()
                date_ranges.append(set([start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]))
            else:
                date = parse(word).replace(year=datetime.now().year).date()
                date_ranges.append(set([date]))
        except ValueError:
            continue
    return date_ranges
