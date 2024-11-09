from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from config import LOG_CHANNEL_ID, TELEGRAM_BOT_TOKEN
from telegram import Bot

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def log_message(message):
    """Send a log message to the specified log channel."""
    bot.send_message(chat_id=LOG_CHANNEL_ID, text=message)

def start_command(update: Update, context: CallbackContext):
    """Handle the /start command."""
    user = update.effective_user
    welcome_message = f"Welcome, {user.first_name}! How can I assist you today?"
    update.message.reply_text(welcome_message)
    
    # Log the start command
    log_message(f"/start command received from {user.username} ({user.id})")

def help_command(update: Update, context: CallbackContext):
    """Handle the /help command."""
    help_text = "Here are the commands you can use:\n/start - Start the bot\n/help - Get help"
    update.message.reply_text(help_text)
    
    # Log the help command
    log_message(f"/help command received from {update.effective_user.username} ({update.effective_user.id})")

def echo_message(update: Update, context: CallbackContext):
    """Echo the user message."""
    user_message = update.message.text
    update.message.reply_text(user_message)
    
    # Log the echoed message
    log_message(f"Echoed message from {update.effective_user.username} ({update.effective_user.id}): {user_message}")

def unknown_command(update: Update, context: CallbackContext):
    """Handle unknown commands."""
    update.message.reply_text("Sorry, I didn't understand that command.")
    
    # Log the unknown command
    log_message(f"Unknown command received from {update.effective_user.username} ({update.effective_user.id})")

# Create a list of handlers
def get_handlers():
    """Return a list of command and message handlers."""
    return [
        CommandHandler('start', start_command),
        CommandHandler('help', help_command),
        MessageHandler(Filters.text & ~Filters.command, echo_message),
        MessageHandler(Filters.command, unknown_command),
    ]
