from bot import Bot
from database.db_handler import create_database

# Initialize the database
create_database()

# Initialize and run the bot
Bot().run()
