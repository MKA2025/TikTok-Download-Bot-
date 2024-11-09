# src/bot.py

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from downloader import download_tiktok_video
from config import TELEGRAM_BOT_TOKEN

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("👋 Hi, I am a bot for downloading TikTok videos without watermark. Please send the video link.")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    url = update.message.text
    if 'tiktok.com' in url:
        update.message.reply_text("⏳ Please wait while I download the video...")

        video_url = download_tiktok_video(url)
        if video_url:
            context.bot.send_video(chat_id=update.message.chat_id, video=video_url)
        else:
            update.message.reply_text("❌ Sorry, I couldn't download the video. Please try again later.")
    else:
        update.message.reply_text("❌ Please send a valid TikTok video link.")

def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
