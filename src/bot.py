import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import requests

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
    log_message(f"Received video URL: {video_url}")

    # Add logic to download the TikTok video here
    # Example: video_data = requests.get(video_url)

    # Send the video back to the user
    # update.message.reply_video(video_data)

    # Delete the video after sending
    # os.remove(video_path)  # Replace video_path with your video file path

# Register command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

# Start the bot
updater.start_polling()
updater.idle()
