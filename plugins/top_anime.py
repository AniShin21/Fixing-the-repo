import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from helper_func import subscribed, decode, get_messages

# Function to fetch top anime from MyAnimeList
# I know That You're Going To Steel This Featur 
# If Your steel this featre then import only def command that are give below 
# Bro I will recommant that make your own script you bastared
def fetch_top_anime():
    url = 'https://myanimelist.net/topanime.php?type=bypopularity'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract anime titles from the page
    titles = soup.select('.ranking-list .title .hoverinfo_trigger')
    top_anime = [title.get_text().strip() for title in titles[:10]]  # Get top 10 anime titles
    
    return top_anime

@Bot.on_message(filters.command('top_anime') & filters.private & subscribed)
async def top_anime_command(client: Client, message: Message):
    try:
        top_anime_list = fetch_top_anime()
        response_message = "*Top Anime of July 2024:*\n\n" + "\n".join(f"{i+1}. {anime}" for i, anime in enumerate(top_anime_list))
        await message.reply_text(response_message, parse_mode="markdown")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
