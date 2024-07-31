import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from helper_func import subscribed, decode, get_messages
from database.database import present_user, add_user

# Function to fetch top anime from MyAnimeList
# I know That You're Going to Steel This Feature if you steel i will seguest you use chatgpt (  🥺🥳✅👇   )
# If Your steel this feature then import only def command that are give below               \| Chatgpt.con |/
# Bro I will recommant that make your own script you %#$#$##***
# If You Get Any Error Then Contact me i will not help you 
# I Will Help But Only If You Pay Me ( Just kidding bro i am not serious )
# Contact Me @iTz_Anayokoji
# Function to scrape the top anime of the month
def scrape_top_anime():
    url = 'https://myanimelist.net/topanime.php'  # URL of the site to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the top anime list
    top_anime_list = []
    for i, anime in enumerate(soup.select('.ranking-list .title .link-title'), start=1):
        if i > 5:  # Limit to top 5
            break
        anime_title = anime.text.strip()
        top_anime_list.append(f"{i}. {anime_title}")
    
    return "\n".join(top_anime_list)

# Command handler for /top_anime using the provided structure
@Bot.on_message(filters.command('top_anime') & filters.private)
async def top_anime_command(client: Client, message: Message):
    id = message.from_user.id
    # Here you can add logic for user validation if needed
    top_anime_list = scrape_top_anime()
    await message.reply_text(f"Top Anime of this Month:\n{top_anime_list}")
