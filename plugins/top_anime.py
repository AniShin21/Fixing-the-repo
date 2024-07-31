import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from helper_func import subscribed, decode, get_messages

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
        response_message = "*Top Anime of July 2024:*\n\n" + "\n".join(f"{i+1}. {anime}" for i, anime in enumerate(top_anime_list))
        await message.reply_text(response_message, parse_mode="Markdown")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

# Assuming you have a similar start command
@Client.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        # Additional logic here
        pass
