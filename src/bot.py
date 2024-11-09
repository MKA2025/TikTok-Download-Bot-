import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
LOG_CHANNEL_ID = '@your_channel_username'  # Replace with your channel username or ID

# Initialize the bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Set up logging
logging.basicConfig(level=logging.INFO)

def log_message(message):
    """Send a log message to the specified channel."""
    try:
        updater.bot.send_message(chat_id=LOG_CHANNEL_ID, text=message)
        logging.info(f"Log sent to {LOG_CHANNEL_ID}: {message}")
    except Exception as e:
        logging.error(f"Failed to send log message: {e}")

def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    update.message.reply_text('Welcome! Please provide a TikTok video link to download.')

def download_video(update: Update, context: CallbackContext):
    """Download the TikTok video from the provided link."""
    video_url = update.message.text
    quality = context.args[0] if context.args else 'high'  # Default to 'high' quality if not specified
    log_message(f"Received video URL: {video_url} with quality: {quality}")

    # Validate quality input
    valid_qualities = ['low', 'medium', 'high']
    if quality not in valid_qualities:
        update.message.reply_text("Invalid quality specified. Please use 'low', 'medium', or 'high'.")
        return

    try:
        # Example: Use a TikTok video downloader API or library
        api_url = f'https://api.tikwm.com/video?url={video_url}&quality={quality}'  # Hypothetical API endpoint
        response = requests.get(api_url)

        if response.status_code == 200:
            # Assuming the response contains the video data
            video_file_path = 'downloaded_video.mp4'  # Temporary file path
            with open(video_file_path, 'wb') as video_file:
                video_file.write(response.content)

            # Send the video back to the user
            with open(video_file_path, 'rb') as video_file:
                update.message.reply_video(video_file)

            # Log the successful download
            log_message(f"Video downloaded and sent to {update.effective_user.username}")

            # Delete the video after sending
            os.remove(video_file_path)
        else:
            update.message.reply_text("Failed to download the video. Please check the link.")
            log_message(f"Failed to download video from {video_url}: {response.status_code}")

    except Exception as e:
        update.message.reply_text("An error occurred while downloading the video.")
        log_message(f"Error downloading video: {e}")

# Register command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

# Start the bot
updater.start_polling()
updater.idle()
