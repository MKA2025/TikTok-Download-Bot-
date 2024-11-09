# tests/test_bot.py

import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message
from telegram.ext import CallbackContext
from src.bot import start, handle_message

class TestTelegramBot(unittest.TestCase):

    @patch('src.bot.Update')
    @patch('src.bot.CallbackContext')
    def test_start_command(self, mock_context, mock_update):
        # Create a mock update object
        mock_update.message = MagicMock()
        mock_update.message.reply_text = MagicMock()

        # Call the start function
        start(mock_update, mock_context)

        # Assert that the reply_text method was called with the correct message
        mock_update.message.reply_text.assert_called_once_with("👋 Hi, I am a bot for downloading TikTok videos without watermark. Please send the video link.")

    @patch('src.bot.download_tiktok_video')
    @patch('src.bot.Update')
    @patch('src.bot.CallbackContext')
    def test_handle_message_valid_url(self, mock_context, mock_update, mock_download):
        # Create a mock update object with a valid TikTok URL
        mock_update.message = MagicMock()
        mock_update.message.text = 'https://www.tiktok.com/@user/video/1234567890'
        mock_update.message.reply_text = MagicMock()
        mock_context.bot.send_video = MagicMock()

        # Mock the download function to return a video URL
        mock_download.return_value = 'https://example.com/video.mp4'

        # Call the handle_message function
        handle_message(mock_update, mock_context)

        # Assert that the reply_text method was called with the correct message
        mock_context.bot.send_video.assert_called_once_with(chat_id=mock_update.message.chat_id, video='https://example.com/video.mp4')

    @patch('src.bot.download_tiktok_video')
    @patch('src.bot.Update')
    @patch('src.bot.CallbackContext')
    def test_handle_message_invalid_url(self, mock_context, mock_update, mock_download):
        # Create a mock update object with an invalid URL
        mock_update.message = MagicMock()
        mock_update.message.text = 'https://www.example.com'
        mock_update.message.reply_text = MagicMock()

        # Call the handle_message function
        handle_message(mock_update, mock_context)

        # Assert that the reply_text method was called with the correct error message
        mock_update.message.reply_text.assert_called_once_with("❌ Please send a valid TikTok video link.")

    @patch('src.bot.download_tiktok_video')
    @patch('src.bot.Update')
    @patch('src.bot.CallbackContext')
    def test_handle_message_download_failure(self, mock_context, mock_update, mock_download):
        # Create a mock update object with a valid TikTok URL
        mock_update.message = MagicMock()
        mock_update.message.text = 'https://www.tiktok.com/@user/video/1234567890'
        mock_update.message.reply_text = MagicMock()

        # Mock the download function to return None (indicating failure)
        mock_download.return_value = None

        # Call the handle_message function
        handle_message(mock_update, mock_context)

        # Assert that the reply_text method was called with the correct error message
        mock_update.message.reply_text.assert_called_once_with("❌ Sorry, I couldn't download the video. Please try again later.")

if __name__ == '__main__':
    unittest.main()
