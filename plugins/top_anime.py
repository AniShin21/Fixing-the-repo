import requests
from bs4 import BeautifulSoup
from pyrofork import Client, filters
from pyrofork.types import Message
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
def fetch_top_anime():
    url = 'https://myanimelist.net/topanime.php?type=bypopularity'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract anime titles from the page
    titles = soup.select('.ranking-list .title .hoverinfo_trigger')
    top_anime = [title.get_text().strip() for title in titles[:10]]  # Get top 10 anime titles
    
    return top_anime

@Client.on_message(filters.command('top_anime') & filters.private)
async def top_anime_command(client: Client, message: Message):
    try:
        top_anime_list = fetch_top_anime()
        response_message = "*Top Anime of July 2024:*\n\n" + "\n".join(f"{i+1}. {anime.replace('.', '\\.').replace('-', '\\-').replace('_', '\\_')}" for i, anime in enumerate(top_anime_list))
        await message.reply_text(response_message, parse_mode="MarkdownV2")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
