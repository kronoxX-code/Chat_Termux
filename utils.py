# utils.py
import os
import time
from config import Colors, EMOJIS

def clear_screen():
    os.system('clear')

def print_header():
    print(f"{Colors.CYAN}┌────────────────────────────────────────┐")
    print(f"│           KRONOX-CHAT v3.0              │")
    print(f"└────────────────────────────────────────┘{Colors.RESET}")

def format_time():
    return time.strftime("%H:%M")

def replace_emojis(text):
    for code, emoji in EMOJIS.items():
        text = text.replace(code, emoji)
    return text

def get_user_color(username):
    colors = ['RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN']
    color_index = sum(ord(c) for c in username) % len(colors)
    return colors[color_index]
