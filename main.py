from datetime import datetime
import os
import subprocess
import time
import random

from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.markdown import Markdown
from rich.console import Group
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.text import Text
import rich

random.seed(123)

layout = Layout()
layout.split(
    Layout(name="header", size=3),
    Layout(name="main", ratio=5),
)

layout["main"].split_row(
    Layout(name="side", ratio=1),
    # Layout(Panel(""), name="notmiddle", ratio=0),
    Layout(name="body", ratio=2),
)

COLORS = [
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
]
USER_COLORS = {}


def get_user_color(username):
    if username not in USER_COLORS:
        USER_COLORS[username] = random.choice(COLORS)
    return USER_COLORS[username]


last_message_count = -1
last_notification_time = datetime.min


def make_messages():
    global last_message_count, last_notification_time
    """messages.log -> messages panel"""
    messages = []
    try:
        with open("messages.log", "r") as f:
            for line in f:
                if "," in line:
                    username, message = line.strip().split(",", 1)
                    color = get_user_color(username)
                    messages.append(
                        Text.from_markup(f"[bold {color}]{username}[/]: {message}")
                    )

        if (
            last_message_count != -1
            and len(messages) > last_message_count
            and (datetime.now() - last_notification_time).total_seconds() > 5
        ):
            print("SOUND")
            sound_file = os.path.expanduser(os.getenv("SOUNDFILE", "~/metal.wav"))
            subprocess.Popen(["aplay", sound_file])
            last_notification_time = datetime.now()

        last_message_count = len(messages)

    except FileNotFoundError:
        return Panel(Text("messages.log not found", style="red"))
    return Panel(Group(*messages), title="#what-the-slack")


def make_header():
    timestamp = datetime.now().strftime("%a %b %d %H[blink]:[/]%M[blink]:[/]%S %Y")
    sublayout = Layout()
    sublayout.split_row(Layout(Markdown("# test")), Layout(Panel(timestamp)))
    return sublayout


with Live(layout, refresh_per_second=4, screen=True):

    while True:
        layout["header"].update(make_header())
        layout["side"].update(make_messages())
        layout["body"].update(
            Panel(
                Text.from_ansi(
                    subprocess.run(
                        [
                            "fastfetch",
                            "--structure",
                            "OS:Host:Uptime:Packages:CPU:Memory:Disk",
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                        timeout=10,
                    ).stdout
                ),
            )
        )

        time.sleep(0.25)
