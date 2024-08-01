from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import sqlite3
import requests

def create_database():
    conn = sqlite3.connect('anime_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weekly_anime (
            week TEXT PRIMARY KEY,
            top_anime TEXT
        )
    ''')
    conn.commit()
    conn.close()

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
        return data['data']['Page']['media']
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
        return data['data']['Page']['media']
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
        return data['data']['Page']['media']
    return None

async def top_anime(client: Client, message: Message):
    keyboard = [
        [InlineKeyboardButton("Weekly Top Anime", callback_data='weekly')],
        [InlineKeyboardButton("Trending Anime", callback_data='trending')],
        [InlineKeyboardButton("Top Anime List", callback_data='top')]
    ]
    await message.reply_text("Select the category:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    if data == 'weekly':
        anime_list = get_weekly_top_anime()
    elif data == 'trending':
        anime_list = get_trending_anime()
    elif data == 'top':
        anime_list = get_top_anime_list()
    else:
        await callback_query.answer("Invalid selection.")
        return

    if not anime_list:
        await callback_query.message.edit_text("No data available.")
        return

    response_text = ""
    for anime in anime_list[:10]:
        title = anime['title']['romaji']
        if anime['title']['english']:
            title += f" ({anime['title']['english']})"
        response_text += f"• {title}\n"

    await callback_query.message.edit_text(response_text)

def create_database():
    conn = sqlite3.connect('anime_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weekly_anime (
            week TEXT PRIMARY KEY,
            top_anime TEXT
        )
    ''')
    conn.commit()
    conn.close()

