from ..utils.logger import logger
from ..utils.constants import CHANNEL_ID

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    )
from telegram.ext import(
    ContextTypes, 
    CallbackContext
    )
import os


def process_message(message):
    # aff headiline to the message
    headline = "חדשות ישראל IL - בטלגרם "
    news_link = "https://t.me/newsi_l"
    return f"{message}\n\n{headline}\n{news_link}"
    
 # Function to list images in the /data/headlines folder and create a keyboard
async def list_images(update: Update, context: CallbackContext):
        keyboard = []
        image_files = os.listdir('data/headlines')

        for index, image in enumerate(image_files):
            # Each button has the text of the image filename and a callback data
            keyboard.append([InlineKeyboardButton(image, callback_data=str(index))])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Please choose a headline image:', reply_markup=reply_markup)

# Callback function to handle the selection of an image
def handle_image_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # This is the index of the selected image
    selected_image_index = int(query.data)

    # Store this index in the user's context for later use
    context.user_data['selected_image_index'] = selected_image_index

    # Now ask the user for the text to accompany the image
    query.edit_message_text(text="Please send me the text for the headline.")

# Callback function to handle the selection of an image
async def handle_image_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Extracting the selected image index
    selected_image_index = int(query.data)

    # Store this index in the user's context for later use
    context.user_data['selected_image_index'] = selected_image_index

    # Inform the user to send the text
    await query.edit_message_text(text="הוסף את הכותרת לתמונה.")

async def post_headline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('post_headline')
    selected_image_index = context.user_data.get('selected_image_index')
    text = update.message.text

    if selected_image_index is not None and text:
        image_files = os.listdir('data/headlines')
        selected_image = image_files[selected_image_index]

        # Send the photo with the user's text
        with open(f'data/headlines/{selected_image}', 'rb') as photo:
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=text)

        # Clear the selected image index for the next use
        del context.user_data['selected_image_index']
    else:
        await update.message.reply_text("Something went wrong. Please try the command again.")
        