from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_handler import get_weekly_top_anime, get_trending_anime, get_top_anime_list

async def handle_callback(client, callback_query):
    data = None
    if callback_query.data == 'weekly':
        data = get_weekly_top_anime()
    elif callback_query.data == 'trending':
        data = get_trending_anime()
    elif callback_query.data == 'top':
        data = get_top_anime_list()

    if data:
        message_lines = [f"{i+1}. {anime['title']['romaji']} ({anime['title']['english']})"
                         for i, anime in enumerate(data)]
        message = "\n".join(message_lines)
    else:
        message = 'No data available.'

    await callback_query.message.edit_text(message)

async def top_anime(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Weekly Top Anime", callback_data='weekly')],
        [InlineKeyboardButton("Trending Anime", callback_data='trending')],
        [InlineKeyboardButton("Top Anime List", callback_data='top')]
    ])
    await message.reply("Please choose:", reply_markup=keyboard)
