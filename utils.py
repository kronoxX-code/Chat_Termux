# utils.py
import os
import time
import random
from config import Colors, EMOJIS, ROOMS

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_kronox_banner():
    banner = f"""
{Colors.KRONOX_CYAN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║  {Colors.KRONOX_RED}▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_ORANGE}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_YELLOW}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_GREEN}▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_CYAN}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_BLUE}▓▓▓▓▓▓▓▓▓▓  ║
    ║  {Colors.KRONOX_RED}▓▓     ▓▓  {Colors.KRONOX_ORANGE}▓▓      ▓▓  {Colors.KRONOX_YELLOW}▓▓      ▓▓  {Colors.KRONOX_GREEN}▓▓     ▓▓  {Colors.KRONOX_CYAN}▓▓      ▓▓  {Colors.KRONOX_BLUE}▓▓     ▓▓  ║
    ║  {Colors.KRONOX_RED}▓▓     ▓▓  {Colors.KRONOX_ORANGE}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_YELLOW}▓▓      ▓▓  {Colors.KRONOX_GREEN}▓▓     ▓▓  {Colors.KRONOX_CYAN}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_BLUE}▓▓     ▓▓  ║
    ║  {Colors.KRONOX_RED}▓▓     ▓▓  {Colors.KRONOX_ORANGE}▓▓      ▓▓  {Colors.KRONOX_YELLOW}▓▓      ▓▓  {Colors.KRONOX_GREEN}▓▓     ▓▓  {Colors.KRONOX_CYAN}▓▓      ▓▓  {Colors.KRONOX_BLUE}▓▓     ▓▓  ║
    ║  {Colors.KRONOX_RED}▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_ORANGE}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_YELLOW}▓▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_GREEN}▓▓▓▓▓▓▓▓▓▓  {Colors.KRONOX_CYAN}▓▓      ▓▓  {Colors.KRONOX_BLUE}▓▓▓▓▓▓▓▓▓▓  ║
    ║                                                                ║
    ║                {Colors.KRONOX_PURPLE}🛰️  S I S T E M A  D E  C O M U N I C A C I O N E S  🛰️            {Colors.RESET}  ║
    ║                                                                ║
    ║    {Colors.KRONOX_GREEN}Versión 3.0 - Secure Terminal Communication Protocol    {Colors.RESET}      ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

def print_chat_header(room="general", user_count=0):
    room_name = ROOMS.get(room, room)
    header = f"""
{Colors.KRONOX_CYAN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════════════╗
    ║  {Colors.KRONOX_GREEN}🛰️  SALA: {room_name:<25} 👥 USUARIOS: {user_count:>3}     {Colors.KRONOX_CYAN}║
    ║  {Colors.KRONOX_YELLOW}⏰ INICIO: {time.strftime('%Y-%m-%d %H:%M:%S'):<38} {Colors.KRONOX_CYAN}║
    ╚════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(header)

def print_message_box():
    print(f"{Colors.KRONOX_BLUE}{Colors.BOLD}")
    print("    ╔═══════════════════════════════ MENSAJES ═══════════════════════════════╗")
    print(f"{Colors.RESET}")

def print_input_prompt(username, room):
    prompt = f"""
{Colors.KRONOX_GREEN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════════════╗
    ║  {Colors.KRONOX_CYAN}💬 {username}@{room}>{Colors.KRONOX_YELLOW} {Colors.RESET}"""
    print(prompt, end='')

def format_time():
    return time.strftime("%H:%M:%S")

def replace_emojis(text):
    for code, emoji in EMOJIS.items():
        text = text.replace(code, emoji)
    return text

def get_user_color(username):
    colors = ['KRONOX_RED', 'KRONOX_ORANGE', 'KRONOX_YELLOW', 'KRONOX_GREEN', 
              'KRONOX_CYAN', 'KRONOX_BLUE', 'KRONOX_PURPLE', 'KRONOX_PINK']
    color_index = sum(ord(c) for c in username) % len(colors)
    return colors[color_index]

def generate_id():
    return f"KRX-{random.randint(1000, 9999)}"