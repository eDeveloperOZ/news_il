from ..utils.logger import logger
from ..utils.constants import CHANNEL_ID

from telegram import Update
from telegram.ext import ContextTypes

from PIL import Image
import os
import requests
from io import BytesIO
import tempfile
from moviepy.editor import ImageClip, CompositeVideoClip, VideoFileClip


def process_message(message):
    # Add headline to the message
    command_text = '/post_newssil'
    headline = "חדשות ישראל IL - בטלגרם "
    news_link = "https://t.me/newssil"
    if command_text in message:
        # remove the command text
        message = message.replace(command_text, "")
    return f"{message}\n\n{headline}\n{news_link} "

async def overlay_sticker_on_photo(photo_file_id, context):
    # Download the photo
    file = await context.bot.getFile(photo_file_id)
    photo_bytes = requests.get(file.file_path).content
    photo_image = Image.open(BytesIO(photo_bytes))

    # Overlay the sticker
    sticker_path = "data/sticker.webp"
    sticker_image = Image.open(sticker_path).convert("RGBA")
    photo_image.paste(sticker_image, (0, 0), sticker_image)

    # Convert to bytes for upload
    modified_photo_bytes = BytesIO()
    photo_image.save(modified_photo_bytes, format='PNG')
    modified_photo_bytes.seek(0)

    return modified_photo_bytes

async def overlay_sticker_on_video(video_file_id, context):
    # Download the video
    file = await context.bot.getFile(video_file_id)
    video_bytes = requests.get(file.file_path).content

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(video_bytes)
        temp_video_file_path = temp_video_file.name

    # Process the video
    video_clip = VideoFileClip(temp_video_file_path)
    
    # Overlay the sticker
    sticker_path = "data/sticker.webp"
    sticker_clip = ImageClip(sticker_path, duration=video_clip.duration).set_position(("center", "center"))
    final_clip = CompositeVideoClip([video_clip, sticker_clip])

    # Write to a temporary output file
    output_path = tempfile.mktemp(suffix=".mp4")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Clean up the temporary input file
    os.remove(temp_video_file_path)

    return output_path

async def post_newssil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('post_news_il')
    message = update.message

    # Process Text Message
    if message.text:
        processed_text = process_message(message.text)
        await context.bot.send_message(chat_id=CHANNEL_ID, text=processed_text, disable_web_page_preview=True)

    # Process Photo
    elif message.photo:
        photo = message.photo[-1]  # Highest resolution photo
        caption = process_message(message.caption) if message.caption else ""
        modified_photo = await overlay_sticker_on_photo(photo.file_id, context)
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=modified_photo, caption=caption)

    # Process Video
    elif message.video:
        # Handling for videos would be added here
        caption = process_message(message.caption) if message.caption else ""
        modified_video = await overlay_sticker_on_video(message.video.file_id, context)
        with open(modified_video, 'rb') as video_file:
            await context.bot.send_video(chat_id=CHANNEL_ID, video=video_file, caption=caption)

    # Process Audio 
    elif message.audio:
        caption = process_message(message.caption) if message.caption else ""
        await context.bot.send_audio(chat_id=CHANNEL_ID, audio=message.audio.file_id, caption=caption)
