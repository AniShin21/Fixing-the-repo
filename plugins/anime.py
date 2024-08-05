import os
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot

# These are some commands to handel functions of API

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

# Command handler to display top anime
@Bot.on_message(filters.command('top') & filters.private)
async def top_anime_command(client: Client, message: Message):
    try:
        top_anime_list = get_top_anime()
        if not top_anime_list:
            await message.reply("No top anime found at the moment.")
            return

        anime_info = ""
        for anime in top_anime_list[:10]:  # Display top 10 anime
            title = anime.get("title")
            url = anime.get("url")
            score = anime.get("score")
            anime_info += f"🔹 <a href='{url}'>{title}</a> - Score: {score}\n"

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("View More", url="https://myanimelist.net/topanime.php")]
            ]
        )
        
        await message.reply_text(
            f"<b>Top Anime:</b>\n\n{anime_info}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Command handler to display weekly anime
@Bot.on_message(filters.command('weekly') & filters.private)
async def weekly_anime_command(client: Client, message: Message):
    try:
        weekly_anime_list = get_weekly_anime()
        if not weekly_anime_list:
            await message.reply("No weekly anime found at the moment.")
            return

        anime_info = ""
        for anime in weekly_anime_list[:10]:  # Display top 10 weekly anime
            title = anime.get("title")
            url = anime.get("url")
            score = anime.get("score")
            anime_info += f"🔹 <a href='{url}'>{title}</a> - Score: {score}\n"

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("View More", url="https://myanimelist.net/season")]
            ]
        )
        
        await message.reply_text(
            f"<b>Weekly Anime:</b>\n\n{anime_info}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Command handler to search for anime
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

        anime_info = ""
        for anime in search_results[:10]:  # Display top 10 search results
            title = anime.get("title")
            url = anime.get("url")
            score = anime.get("score")
            anime_info += f"🔹 <a href='{url}'>{title}</a> - Score: {score}\n"

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("View More", url="https://myanimelist.net/search/all?q=" + query)]
            ]
        )
        
        await message.reply_text(
            f"<b>Search Results for '{query}':</b>\n\n{anime_info}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
