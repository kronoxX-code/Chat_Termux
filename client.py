# client.py
import socket
import threading
import sys
import os
from config import Colors, COMMANDS
from utils import clear_screen, print_header, replace_emojis

class KronoxChatClient:
    def __init__(self):
        self.nickname = ""
        self.client = None
        self.connected = False
        self.current_room = "general"
        
    def connect(self, host, port):
        try:
            clear_screen()
            print_header()
            
            print(f"{Colors.CYAN}🔗 Conectando a {host}:{port}...{Colors.RESET}")
            
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
            self.connected = True
            
            # Obtener nickname
            self.nickname = input(f"{Colors.YELLOW}🎯 Tu nickname: {Colors.RESET}")
            
            # Iniciar hilo de recepción
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.show_chat_interface()
            self.write_loop()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
            input("Enter para salir...")
    
    def show_chat_interface(self):
        clear_screen()
        print_header()
        print(f"{Colors.GREEN}✅ Conectado como: {self.nickname}{Colors.RESET}")
        print(f"{Colors.BLUE}💬 Sala: {self.current_room}{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 Escribe /help para comandos{Colors.RESET}")
        print(f"{Colors.CYAN}────────────────────────────────────────────{Colors.RESET}")
    
    def receive(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(f"\r{message}\n{self.get_input_prompt()}", end='')
            except:
                if self.connected:
                    print(f"\n{Colors.RED}❌ Conexión perdida{Colors.RESET}")
                self.connected = False
                break
    
    def get_input_prompt(self):
        return f"{Colors.GREEN}{self.nickname}>{Colors.RESET} "
    
    def write_loop(self):
        while self.connected:
            try:
                message = input(self.get_input_prompt())
                
                if message.startswith('/'):
                    self.handle_command(message)
                else:
                    message = replace_emojis(message)
                    self.client.send(message.encode('utf-8'))
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 Saliendo...{Colors.RESET}")
                self.client.send('/quit'.encode('utf-8'))
                self.connected = False
                break
            except Exception as e:
                print(f"\n{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    def handle_command(self, message):
        if message.lower() in ['/quit', '/exit']:
            print(f"{Colors.YELLOW}👋 Saliendo...{Colors.RESET}")
            self.client.send('/quit'.encode('utf-8'))
            self.connected = False
            return
        
        elif message.lower() == '/clear':
            self.show_chat_interface()
            return
        
        elif message.lower() == '/help':
            self.show_help()
            return
        
        # Enviar comando al servidor
        self.client.send(message.encode('utf-8'))
    
    def show_help(self):
        help_text = f"\n{Colors.CYAN}📖 Comandos:{Colors.RESET}\n"
        for cmd, desc in COMMANDS.items():
            help_text += f"  {Colors.GREEN}{cmd:<8}{Colors.RESET} {desc}\n"
        print(help_text)

def main():
    if len(sys.argv) != 3:
        print(f"{Colors.CYAN}Uso: python client.py <host> <puerto>{Colors.RESET}")
        print(f"{Colors.YELLOW}Ejemplo: python client.py 192.168.1.10 8080{Colors.RESET}")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    client = KronoxChatClient()
    client.connect(host, port)

if __name__ == "__main__":
    main()
