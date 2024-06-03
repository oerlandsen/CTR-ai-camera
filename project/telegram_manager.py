import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramManager:

    def __init__(
        self,
        message: str,
        max_frame: int = 20
    ) -> None:
        """
        Initialize the TelegramManager object.

        Args:
            message (str): The message to send when the alarm is triggered.
            max_frame (int, optional): The maximum number of frames to wait before sending the message. Defaults to 20.
        """
        self.alarm_frames = 0
        self.alarm = False

        self.message = message
        self.max_frame = max_frame

    def analyze(self, ai_result) -> None:
        """
        Analyze the AI result and send a message if the alarm is triggered.

        Args:
            ai_result: AI Result object with the alarm attribute.
        """
        if ai_result.alarm:
            self.alarm = True
            self.alarm_frames += 1
        
        if self.alarm and self.alarm_frames == self.max_frame:
            self.send_message()
            self.alarm_frames = 0
       
        if not ai_result.alarm:
            self.alarm = False
            self.alarm_frames = 0

    def send_message(self) -> dict:
        """
        Send a message to a telegram chat.

        Args:
            message (str): The message to send.
            chat_id (str): The chat id to send the message to. If None, the TELEGRAM_CHAT_ID environment variable will be used.
            token (str): The token to use to send the message. If None, the TELEGRAM_TOKEN environment variable will be used.
        """
        TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
        TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

        print(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": self.message
        }

        response = requests.post(url, data=data)
        
        return response.json()
