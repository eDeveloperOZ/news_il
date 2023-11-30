from .utils.constants import ACCESS_TOKEN
from .utils.logger import logger
from .commands.post_news_il import post_newssil
from .commands.post_headline import *

from telegram import (
    Bot,
    Update
    )
from telegram.ext import(
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler, 
    filters,
    Application
)

def run_bot():
    bot = Bot(token=ACCESS_TOKEN)

    application = Application.builder().token(ACCESS_TOKEN).build()

    # Command handler for /post_news_il
    news_il_handler = CommandHandler('post_newssil', post_newssil)
    application.add_handler(news_il_handler)

    # Message handler for photos with captions
    photo_handler = MessageHandler(filters.PHOTO & filters.CAPTION, post_newssil)
    application.add_handler(photo_handler)

    # Message handler for videos with captions
    video_handler = MessageHandler(filters.VIDEO & filters.CAPTION, post_newssil)
    application.add_handler(video_handler)

    # Command handler for /post_headline
    headline_command_handler = CommandHandler('post_headline', list_images)
    application.add_handler(headline_command_handler)

    # Callback query handler for inline keyboard selections
    callback_query_handler = CallbackQueryHandler(handle_image_selection)
    application.add_handler(callback_query_handler)

    # Message handler for headline text messages
    headline_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, post_headline)
    application.add_handler(headline_handler)

    # Start the Bot
    application.run_polling()