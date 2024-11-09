from telegram import Update
from telegram.ext import CallbackContext
from config import LOG_CHANNEL_ID, TELEGRAM_BOT_TOKEN
from telegram import Bot

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def log_message(message):
    """Send a log message to the specified log channel."""
    bot.send_message(chat_id=LOG_CHANNEL_ID, text=message)

def handle_error(update: Update, context: CallbackContext):
    """Log errors that occur in the bot."""
    # Create an error message
    error_message = f"Error occurred: {context.error}"

    # Log the error message to the log channel
    log_message(error_message)

    # Optionally, log the update that caused the error
    if update:
        log_message(f"Update that caused the error: {update}")

    # Optionally, you can send a user-friendly message to the user
    if update.effective_chat:
        update.effective_chat.send_message("An error occurred while processing your request. Please try again later.")
