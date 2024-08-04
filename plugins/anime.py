import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TG_BOT_TOKEN  # Import the token from config.py

# List of websites to search
WEBSITES = [
    'https://graphql.anilist.co',
    'https://kitsu.io/api/edge'
]

def fetch_anime_data(query):
    url = 'https://graphql.anilist.co'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_weekly_top_anime():
    query = '''
    {
      Page {
        media(sort: POPULARITY_DESC, type: ANIME, season: WINTER, seasonYear: 2024) {
          title {
            romaji
            english
          }
          id
        }
      }
    }
    '''
    data = fetch_anime_data(query)
    if data and 'data' in data and 'Page' in data['data']:
        return data['data']['Page']['media'][:5]
    return None

def get_trending_anime():
    query = '''
    {
      Page {
        media(sort: TRENDING_DESC, type: ANIME) {
          title {
            romaji
            english
          }
          id
        }
      }
    }
    '''
    data = fetch_anime_data(query)
    if data and 'data' in data and 'Page' in data['data']:
        return data['data']['Page']['media'][:5]
    return None

def get_top_anime_list():
    query = '''
    {
      Page {
        media(sort: SCORE_DESC, type: ANIME) {
          title {
            romaji
            english
          }
          id
        }
      }
    }
    '''
    data = fetch_anime_data(query)
    if data and 'data' in data and 'Page' in data['data']:
        return data['data']['Page']['media'][:5]
    return None

def search_anime(query):
    results = []
    query_lower = query.lower()

    for website in WEBSITES:
        if website == 'https://graphql.anilist.co':
            search_url = website
            query_data = {'query': f'''
                query {{
                  Page {{
                    media(search: "{query}", type: ANIME) {{
                      title {{
                        romaji
                        english
                      }}
                      id
                    }}
                  }}
                }}
            '''}
        elif website == 'https://kitsu.io/api/edge':
            search_url = f"{website}/anime?filter[name]={query.replace(' ', '+')}"

        try:
            if website == 'https://graphql.anilist.co':
                response = requests.post(search_url, json=query_data)
            else:
                response = requests.get(search_url, timeout=10)

            if response.status_code == 200:
                if website == 'https://graphql.anilist.co':
                    data = response.json()
                    for media in data['data']['Page']['media']:
                        title = media['title']['romaji']
                        results.append({'title': title, 'id': media['id']})
                elif website == 'https://kitsu.io/api/edge':
                    data = response.json()
                    for anime in data['data']:
                        title = anime['attributes']['canonicalTitle']
                        results.append({'title': title, 'id': anime['id']})

        except Exception as e:
            print(f"Error fetching from {website}: {e}")

    if results:
        sorted_results = sorted(results, key=lambda x: x['title'])
        return sorted_results
    return None

async def weekly(update: Update, context: CallbackContext) -> None:
    data = get_weekly_top_anime()
    if data:
        message = "Weekly Top Anime:\n"
        for anime in data:
            message += f"- {anime['title']['romaji']} (ID: {anime['id']})\n"
        if update.message:
            await update.message.reply_text(text=message)
        else:
            await update.callback_query.message.reply_text(text=message)
    else:
        if update.message:
            await update.message.reply_text("No data available.")
        else:
            await update.callback_query.message.reply_text("No data available.")

async def trending(update: Update, context: CallbackContext) -> None:
    data = get_trending_anime()
    if data:
        message = "Trending Anime:\n"
        for anime in data:
            message += f"- {anime['title']['romaji']} (ID: {anime['id']})\n"
        if update.message:
            await update.message.reply_text(text=message)
        else:
            await update.callback_query.message.reply_text(text=message)
    else:
        if update.message:
            await update.message.reply_text("No data available.")
        else:
            await update.callback_query.message.reply_text("No data available.")

async def top(update: Update, context: CallbackContext) -> None:
    data = get_top_anime_list()
    if data:
        message = "Top Anime List:\n"
        for anime in data:
            message += f"- {anime['title']['romaji']} (ID: {anime['id']})\n"
        if update.message:
            await update.message.reply_text(text=message)
        else:
            await update.callback_query.message.reply_text(text=message)
    else:
        if update.message:
            await update.message.reply_text("No data available.")
        else:
            await update.callback_query.message.reply_text("No data available.")

async def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args) if context.args else ''
    if not query:
        if update.message:
            await update.message.reply_text("Please provide a search query.")
        else:
            await update.callback_query.message.reply_text("Please provide a search query.")
        return

    results = search_anime(query)
    if results:
        keyboard = [[InlineKeyboardButton(anime['title'], callback_data=f'detail_{anime["id"]}')] for anime in results]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='start')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message:
            await update.message.reply_text("Select an anime to get details:", reply_markup=reply_markup)
        else:
            await update.callback_query.message.reply_text("Select an anime to get details:", reply_markup=reply_markup)
    else:
        if update.message:
            await update.message.reply_text("No search results found.")
        else:
            await update.callback_query.message.reply_text("No search results found.")

async def details(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    anime_id = query.data.split('_')[1]

    # Fetch detailed information
    query_details = f'''
    {{
      Media(id: {anime_id}) {{
        title {{
          romaji
          english
        }}
        description
        coverImage {{
          extraLarge
        }}
        episodes
        season
        seasonYear
        genres
      }}
    }}
    '''
    data = fetch_anime_data(query_details)
    
    if data and 'data' in data and 'Media' in data['data']:
        anime = data['data']['Media']
        title = anime['title']['romaji']
        english_title = anime['title']['english']
        description = anime['description']
        cover_image = anime['coverImage']['extraLarge']
        episodes = anime['episodes']
        season = anime['season']
        season_year = anime['seasonYear']
        genres = ', '.join(anime['genres'])

        message = (f"*Title:* {title}\n"
                   f"*English Title:* {english_title}\n"
                   f"*Description:* {description}\n"
                   f"*Episodes:* {episodes}\n"
                   f"*Season:* {season} {season_year}\n"
                   f"*Genres:* {genres}\n"
                   f"[Cover Image]({cover_image})")

        keyboard = [
            [InlineKeyboardButton("Back to Search Results", callback_data='search')],
            [InlineKeyboardButton("Back to Main Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(text=message, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await query.message.reply_text("Details not found.")

async def top_anime(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Weekly Top Anime", callback_data='weekly')],
        [InlineKeyboardButton("Trending Anime", callback_data='trending')],
        [InlineKeyboardButton("Top Anime List", callback_data='top')],
        [InlineKeyboardButton("Search for Anime", callback_data='search')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text('Please choose one option:', reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text('Please choose one option:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in ['weekly', 'trending', 'top']:
        command_message = {
            'weekly': 'Use the command /weekly to get the weekly top anime.',
            'trending': 'Use the command /trending to get the trending anime.',
            'top': 'Use the command /top to get the top anime list.'
        }
        await query.message.reply_text(command_message[query.data])
    elif query.data == 'search':
        await search(update, context)
    elif query.data.startswith('detail_'):
        await details(update, context)
    elif query.data == 'start':
        await top_anime(update, context)

def set_bot_commands(token):
    url = f'https://api.telegram.org/bot{token}/setMyCommands'
    commands = [
        {'command': 'top_anime', 'description': 'Show anime options'},
        {'command': 'weekly', 'description': 'Show weekly top anime'},
        {'command': 'trending', 'description': 'Show trending anime'},
        {'command': 'top', 'description': 'Show top anime list'},
        {'command': 'search', 'description': 'Search for an anime'}
    ]
    response = requests.post(url, json={'commands': commands})
    print(response.json())  # For debugging

def main() -> None:
    # Set bot commands
    set_bot_commands(TG_BOT_TOKEN)
    
    # Initialize the application with the token
    application = Application.builder().token(TG_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('top_anime', top_anime))
    application.add_handler(CommandHandler('weekly', weekly))
    application.add_handler(CommandHandler('trending', trending))
    application.add_handler(CommandHandler('top', top))
    application.add_handler(CommandHandler('search', search))
    application.add_handler(CallbackQueryHandler(button, pattern='^start|weekly|trending|top|search|detail_'))

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()
