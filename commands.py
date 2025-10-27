# commands.py
from config import Colors, COMMANDS, EMOJIS
from utils import colorize_text

class CommandHandler:
    def __init__(self, client=None):
        self.client = client
    
    def handle_command(self, command, args=None):
        command = command.lower()
        
        if command == '/help':
            return self.show_help()
        elif command == '/users':
            return self.list_users()
        elif command == '/emoji':
            return self.show_emojis()
        elif command == '/info':
            return self.show_info()
        elif command == '/clear':
            return 'CLEAR'
        else:
            return f"{Colors.RED}Comando no reconocido. Usa /help para ver comandos disponibles.{Colors.RESET}"
    
    def show_help(self):
        help_text = f"\n{Colors.CYAN}{Colors.BOLD}📖 COMANDOS DISPONIBLES:{Colors.RESET}\n"
        help_text += f"{Colors.YELLOW}┌{'─' * 40}┐{Colors.RESET}\n"
        
        for cmd, desc in COMMANDS.items():
            help_text += f"{Colors.YELLOW}│{Colors.RESET} {Colors.GREEN}{cmd:<15}{Colors.RESET} {desc}\n"
        
        help_text += f"{Colors.YELLOW}└{'─' * 40}┘{Colors.RESET}\n"
        return help_text
    
    def show_emojis(self):
        emoji_text = f"\n{Colors.MAGENTA}{Colors.BOLD}😊 EMOJIS DISPONIBLES:{Colors.RESET}\n"
        emoji_text += f"{Colors.YELLOW}┌{'─' * 30}┐{Colors.RESET}\n"
        
        for code, emoji in EMOJIS.items():
            emoji_text += f"{Colors.YELLOW}│{Colors.RESET} {code:<10} → {emoji:<5} {Colors.YELLOW}│{Colors.RESET}\n"
        
        emoji_text += f"{Colors.YELLOW}└{'─' * 30}┘{Colors.RESET}\n"
        return emoji_text
    
    def list_users(self):
        if self.client and hasattr(self.client, 'request_users_list'):
            self.client.request_users_list()
            return "Solicitando lista de usuarios..."
        return "Error: No conectado al servidor"
    
    def show_info(self):
        info = f"""
{Colors.CYAN}{Colors.BOLD}ℹ️  INFORMACIÓN DEL SISTEMA:{Colors.RESET}
{Colors.YELLOW}├─ {Colors.GREEN}Versión: {Colors.WHITE}2.0 Pro
{Colors.YELLOW}├─ {Colors.GREEN}Desarrollado para: {Colors.WHITE}Termux
{Colors.YELLOW}├─ {Colors.GREEN}Características: {Colors.WHITE}
{Colors.YELLOW}│  {Colors.WHITE}• Chat en tiempo real
{Colors.YELLOW}│  {Colors.WHITE}• Mensajes privados
{Colors.YELLOW}│  {Colors.WHITE}• Múltiples salas
{Colors.YELLOW}│  {Colors.WHITE}• Emojis y colores
{Colors.YELLOW}│  {Colors.WHITE}• Interfaz ASCII
{Colors.YELLOW}└─ {Colors.GREEN}Comandos: {Colors.WHITE}/help
"""
        return info