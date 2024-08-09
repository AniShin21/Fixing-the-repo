import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from bot import Bot  # Ensure this imports your Bot class correctly

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
    url = f"https://api.jikan.moe/v4/anime?q={query}&page=1"
    data = fetch_anime_data(url)
    search_results = data.get("data", [])
    return search_results

# Map of anime titles to emojis
anime_emojis = {
    "One Piece": "🏴‍☠️",
    "Naruto": "🥷",
    "Attack on Titan": "🛡️",
    "My Hero Academia": "🦸‍♂️",
    "Demon Slayer": "⚔️",
    "Sword Art Online": "🗡️",
    # Add more mappings as needed
}

# Function to get emoji for anime title
def get_anime_emoji(title):
    for key in anime_emojis:
        if key.lower() in title.lower():
            return anime_emojis[key]
    return "🎬"  # Default emoji

# Cool font style for the anime title
def style_anime_title(title):
    return f"**{title}**".replace("A", "𝔸").replace("B", "𝔹").replace("C", "ℂ").replace("D", "𝔻").replace("E", "𝔼").replace("F", "𝔽").replace("G", "𝔾").replace("H", "ℍ").replace("I", "𝕀").replace("J", "𝕁").replace("K", "𝕂").replace("L", "𝕃").replace("M", "𝕄").replace("N", "ℕ").replace("O", "𝕆").replace("P", "ℙ").replace("Q", "ℚ").replace("R", "ℝ").replace("S", "𝕊").replace("T", "𝕋").replace("U", "𝕌").replace("V", "𝕍").replace("W", "𝕎").replace("X", "𝕏").replace("Y", "𝕐").replace("Z", "ℤ")

# Handler to provide command instructions
@Bot.on_message(filters.command('top_anime') & filters.private)
async def top_anime_instructions(client: Client, message: Message):
    instructions = (
        "Here are the available commands:\n"
        "/top - Display the top anime list.\n"
        "/weekly - Display the current season's anime.\n"
        "/search <query> - Search for an anime."
    )
    await message.reply_text(instructions, parse_mode=ParseMode.HTML)

# Handler to display top anime with buttons
@Bot.on_message(filters.command('top') & filters.private)
async def top_anime_command(client: Client, message: Message):
    try:
        top_anime_list = get_top_anime()
        if not top_anime_list:
            await message.reply("No top anime found at the moment.")
            return

        keyboard = [[InlineKeyboardButton(f"{get_anime_emoji(anime.get('title'))} {anime.get('title')}", callback_data=f'detail_{anime.get("mal_id")}')] 
                    for anime in top_anime_list[:10]]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='top_anime')])
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

        keyboard = [[InlineKeyboardButton(f"{get_anime_emoji(anime.get('title'))} {anime.get('title')}", callback_data=f'detail_{anime.get("mal_id")}')] 
                    for anime in weekly_anime_list[:10]]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='top_anime')])
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

        keyboard = [[InlineKeyboardButton(f"{get_anime_emoji(anime.get('title'))} {anime.get('title')}", callback_data=f'detail_{anime.get("mal_id")}')] 
                    for anime in search_results[:10]]
        keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='top_anime')])
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
        episodes = anime.get("episodes", "N/A")
        score = anime.get("score", "N/A")

        message_text = (f"{style_anime_title(title)}\n\n"
                        f"*Description:* {description}\n"
                        f"*Episodes:* {episodes}\n"
                        f"*Score:* {score}\n")

        keyboard = [
            [InlineKeyboardButton("Back to Top Anime", callback_data='top')],
            [InlineKeyboardButton("Back to Weekly Anime", callback_data='weekly')],
            [InlineKeyboardButton("Back to Search Results", callback_data='search')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await callback_query.message.edit_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await callback_query.message.edit_text(f"An error occurred: {str(e)}")

