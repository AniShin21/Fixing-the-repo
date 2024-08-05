import os
import requests
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, START_MSG
from helper_func import subscribed
from database.database import add_user, present_user

# Function to fetch anime data from the API
def fetch_anime_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

# Function to fetch top anime
def get_top_anime():
    url = "https://api.jikan.moe/v4/top/anime"
    data = fetch_anime_data(url)
    return data['data'][:5]

# Function to fetch weekly anime
def get_weekly_anime():
    url = "https://api.jikan.moe/v4/seasons/now"
    data = fetch_anime_data(url)
    return data['data'][:5]

# Function to search anime based on a query
def search_anime(query):
    url = f"https://api.jikan.moe/v4/anime?q={query}"
    data = fetch_anime_data(url)
    return data['data'][:5]

# Start command handler
@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            return

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Top Anime", callback_data="top"),
                InlineKeyboardButton("Weekly Anime", callback_data="weekly")
            ],
            [
                InlineKeyboardButton("Search Anime", callback_data="search")
            ]
        ]
    )
    await message.reply_text(
        text=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )

# Handler for fetching and displaying top anime
@Bot.on_message(filters.command('top') & filters.private & subscribed)
async def top_anime(client: Client, message: Message):
    top_animes = get_top_anime()
    top_text = "Top Anime:\n\n" + "\n".join([f"{i+1}. {anime['title']}" for i, anime in enumerate(top_animes)])
    await message.reply_text(top_text, disable_web_page_preview=True)

# Handler for fetching and displaying weekly anime
@Bot.on_message(filters.command('weekly') & filters.private & subscribed)
async def weekly_anime(client: Client, message: Message):
    weekly_animes = get_weekly_anime()
    weekly_text = "Weekly Anime:\n\n" + "\n".join([f"{i+1}. {anime['title']}" for i, anime in enumerate(weekly_animes)])
    await message.reply_text(weekly_text, disable_web_page_preview=True)

# Handler for searching anime based on user query
@Bot.on_message(filters.command('search') & filters.private & subscribed)
async def search_anime_handler(client: Client, message: Message):
    query = message.text.split(maxsplit=1)[1]
    search_results = search_anime(query)
    search_text = f"Search Results for '{query}':\n\n" + "\n".join([f"{i+1}. {anime['title']}" for i, anime in enumerate(search_results)])
    await message.reply_text(search_text, disable_web_page_preview=True)
