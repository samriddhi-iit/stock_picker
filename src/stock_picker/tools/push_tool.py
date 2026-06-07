from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushNotificationTool(BaseTool):
    

    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        print(f"Push: {message}")

        if not pushover_user or not pushover_token:
            return '{"notification": "skipped", "reason": "push credentials not configured"}'

        pushover_url = "https://api.pushover.net/1/messages.json"
        payload = {"user": pushover_user, "token": pushover_token, "message": message}
        requests.post(pushover_url, data=payload, timeout=10)
        return '{"notification": "ok"}'