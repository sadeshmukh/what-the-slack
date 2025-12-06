from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging
from dotenv import load_dotenv
import os
import rich

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.event("message")
def handle_message_events(event, say, client):
    if event.get("channel", "") != "C0A2DKARJSD":
        return
    userid = event.get("user")
    text = event.get("text")

    if userid and text:
        user_info = client.users_info(user=userid)
        if user_info.get("bot_id"):
            return
        user_name = (
            user_info["user"]["profile"]["display_name"]
            or user_info["user"]["real_name"]
        )
        with open("messages.log", "a+", buffering=1) as f:
            f.write(f"{user_name},{text}\n")


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()
