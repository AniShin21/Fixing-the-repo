import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from bot import Bot  # Make sure this imports your Bot class correctly

# Function to fetch anime data from the API
def fetch_anime_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

# Function to get top anime
def get_top_anime():
    url = "https://api.jikan.moe/v4/top/anime"
    data = fetch_anime_data(url)
    top_anime_list = data.get("data", [])
    return top_anime_list

# Function to get weekly anime
def get_weekly_anime():
    url = "https://api.jikan.moe/v4/seasons/now"
    data = fetch_anime_data(url)
    weekly_anime_list = data.get("data", [])
    return weekly_anime_list

# Function to search for anime
def search_anime(query):
    url = f"https://api.jikan.moe/v4/search/anime?q={query}&page=1"
    data = fetch_anime_data(url)
    search_results = data.get("data", [])
    return search_results

# Handler to display top anime with buttons
@Bot.on_message(filters.command('top') & filters.private)
async def top_anime_command(client: Client, message: Message):
    try:
        top_anime_list = get_top_anime()
        if not top_anime_list:
            await message.reply("No top anime found at the moment.")
            return

        keyboard = [[InlineKeyboardButton(anime.get("title"), callback_data=f'detail_{anime.get("mal_id")}') 
                     for anime in top_anime_list[:10]]]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            "Top Anime:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Handler to display weekly anime with buttons
@Bot.on_message(filters.command('weekly') & filters.private)
async def weekly_anime_command(client: Client, message: Message):
    try:
        weekly_anime_list = get_weekly_anime()
        if not weekly_anime_list:
            await message.reply("No weekly anime found at the moment.")
            return

        keyboard = [[InlineKeyboardButton(anime.get("title"), callback_data=f'detail_{anime.get("mal_id")}') 
                     for anime in weekly_anime_list[:10]]]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            "Weekly Anime:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Handler to search for anime with buttons
@Bot.on_message(filters.command('search') & filters.private)
async def search_anime_command(client: Client, message: Message):
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply("Please provide a search query.")
        return

    try:
        search_results = search_anime(query)
        if not search_results:
            await message.reply("No anime found for the search query.")
            return

        keyboard = [[InlineKeyboardButton(anime.get("title"), callback_data=f'detail_{anime.get("mal_id")}') 
                     for anime in search_results[:10]]]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            f"Search Results for '{query}':",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Handler to display anime details
@Bot.on_callback_query(filters.regex(r'^detail_'))
async def anime_details(client: Client, callback_query: CallbackQuery):
    anime_id = callback_query.data.split('_')[1]
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    
    try:
        data = fetch_anime_data(url)
        anime = data.get("data", {})
        
        title = anime.get("title")
        description = anime.get("synopsis", "No description available.")
        cover_image = anime.get("images", {}).get("jpg", {}).get("large_image_url", "No cover image")
        episodes = anime.get("episodes", "N/A")
        score = anime.get("score", "N/A")

        message_text = (f"*Title:* {title}\n"
                        f"*Description:* {description}\n"
                        f"*Episodes:* {episodes}\n"
                        f"*Score:* {score}\n"
                        f"[Cover Image]({cover_image})")

        keyboard = [
            [InlineKeyboardButton("Back to Top Anime", callback_data='top')],
            [InlineKeyboardButton("Back to Weekly Anime", callback_data='weekly')],
            [InlineKeyboardButton("Back to Search Results", callback_data='search')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await callback_query.message.reply_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await callback_query.message.reply(f"An error occurred: {str(e)}")
