import time
import requests
from requests.exceptions import RequestException
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes



# Usage
api_key = '7d8adaa96d8668b3a95332f1de1bffc2'
TMDB_BASE_URL = 'https://api.themoviedb.org/3/'
movie_name=''

def get_movie_overview(api_key, movie_name, retries=3):
    url = f"{TMDB_BASE_URL}search/movie"
    params = {
        'api_key': api_key,
        'query': movie_name
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses
            data = response.json()
            if data['results']:
                return data['results'][0].get('overview', 'No description available.')
            else:
                return "Movie not found."
        except RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"Error: {e}"



async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        movie_name = ' '.join(context.args)  # Join arguments to handle spaces in movie names
        
        await update.message.reply_text(get_movie_overview(api_key, movie_name))

        # For demonstration, let's print it to the console
        #print(f'Movie name: {moviename}')
    else:
        await update.message.reply_text('Please provide a movie name. Usage: /movie [moviename]')

# Define your bot token here
TOKEN = '7345673689:AAGWfGfERoUi2BOtUrLh22pYAFZanco2Cqc'
# Set up the Application and Dispatcher
application = Application.builder().token(TOKEN).build()

# Register the command handler
start_handler = CommandHandler('movie', movie)
application.add_handler(start_handler)

# Start the Bot
application.run_polling()
