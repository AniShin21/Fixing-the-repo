# bot.py
# Dont even try to touch me repo
from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, CallbackQuery
import sys
from datetime import datetime
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, CHANNEL_ID, PORT
from plugins.anime import top_anime, handle_callback

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        
        if FORCE_SUB_CHANNEL1:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL1)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL1)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL1)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER.warning(a)
                self.LOGGER.warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER.warning(f"Please Double check the FORCE_SUB_CHANNEL1 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL1}")
                self.LOGGER.info("\nBot Stopped. Contact @iTz_Anayokoji for support")
                sys.exit()
        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER.warning(a)
                self.LOGGER.warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER.warning(f"Please Double check the FORCE_SUB_CHANNEL2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}")
                self.LOGGER.info("\nBot Stopped. Contact @iTz_Anayokoji for support")
                sys.exit()
        if FORCE_SUB_CHANNEL3:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL3)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL3)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL3)).invite_link
                self.invitelink3 = link
            except Exception as a:
                self.LOGGER.warning(a)
                self.LOGGER.warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER.warning(f"Please Double check the FORCE_SUB_CHANNEL3 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL3}")
                self.LOGGER.info("\nBot Stopped. Contact @iTz_Anayokoji for support")
                sys.exit()      
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER.warning(e)
            self.LOGGER.warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER.info("\nBot Stopped. Contact @iTz_Anayokoji for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info(
            f"Bot Running..!\n\nCreated by \n@iTz_Anayokoji")
        self.LOGGER.info(f""" \n\n
        
 █████╗ ███╗   ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗
██╔══██╗████╗  ██║██║██╔════╝██║  ██║██║████╗  ██║
███████║██╔██╗ ██║██║███████╗███████║██║██╔██╗ ██║
██╔══██║██║╚██╗██║██║╚════██║██╔══██║██║██║╚██╗██║
██║  ██║██║ ╚████║██║███████║██║  ██║██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝                 
                                   
                                    """)
        self.username = usr_bot_me.username

        # web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped.")


# Define handler functions outside the class
@Bot.on_message(filters.command('top_anime') & filters.private)
async def top_anime_command(client: Client, message: Message):
    await top_anime(client, message)

@Bot.on_callback_query()
async def handle_callback_query(client: Client, callback_query: CallbackQuery):
    await handle_callback(client, callback_query)


# Initialize and run the bot
app = Bot()
app.run()
