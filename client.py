# client.py
import socket
import threading
import sys
import os
from config import Colors, COMMANDS
from utils import clear_screen, print_kronox_banner, print_chat_header, print_message_box, print_input_prompt
from utils import replace_emojis, get_user_color

class KronoxChatClient:
    def __init__(self):
        self.nickname = ""
        self.client = None
        self.connected = False
        self.current_room = "general"
        
    def connect(self, host, port):
        try:
            clear_screen()
            print_kronox_banner()
            
            print(f"{Colors.KRONOX_CYAN}🔗 CONECTANDO A {host}:{port}...{Colors.RESET}")
            
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
            self.connected = True
            
            # Obtener nickname
            self.nickname = input(f"{Colors.KRONOX_YELLOW}🎯 INGRESE SU IDENTIFICACIÓN: {Colors.RESET}")
            
            # Iniciar hilo de recepción
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.show_chat_interface()
            self.write_loop()
            
        except Exception as e:
            print(f"{Colors.KRONOX_RED}❌ ERROR DE CONEXIÓN: {e}{Colors.RESET}")
            input("Presione Enter para continuar...")
    
    def show_chat_interface(self):
        clear_screen()
        print_kronox_banner()
        print_chat_header(self.current_room, 1)
        print_message_box()
    
    def receive(self):
        while self.connected:
            try:
                message = self.client.recv(4096).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(f"\r{message}\n{self.get_input_line()}", end='')
            except:
                if self.connected:
                    print(f"\n{Colors.KRONOX_RED}❌ CONEXIÓN PERDIDA CON EL SERVIDOR KRONOX{Colors.RESET}")
                self.connected = False
                break
    
    def get_input_line(self):
        return f"{Colors.KRONOX_GREEN}    💬 {self.nickname}@{self.current_room}>{Colors.KRONOX_YELLOW} "
    
    def write_loop(self):
        while self.connected:
            try:
                # Usar input personalizado
                message = input(self.get_input_line())
                
                if message.startswith('/'):
                    self.handle_command(message)
                else:
                    message = replace_emojis(message)
                    self.client.send(message.encode('utf-8'))
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.KRONOX_YELLOW}🛑 DESCONECTANDO DEL SISTEMA KRONOX...{Colors.RESET}")
                self.client.send('/quit'.encode('utf-8'))
                self.connected = False
                break
            except Exception as e:
                print(f"\n{Colors.KRONOX_RED}❌ ERROR: {e}{Colors.RESET}")
    
    def handle_command(self, message):
        if message.lower() in ['/quit', '/exit', '/salir']:
            print(f"{Colors.KRONOX_YELLOW}👋 CERRANDO SESIÓN KRONOX...{Colors.RESET}")
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
        help_text = f"""
{Colors.KRONOX_CYAN}{Colors.BOLD}
    ╔══════════════════════ COMANDOS KRONOX ═══════════════════════╗
    ║                                                                ║
    ║    {Colors.KRONOX_GREEN}COMANDO              DESCRIPCIÓN{Colors.KRONOX_CYAN:<25} ║
    ║    {Colors.KRONOX_YELLOW}────────────────────────────────────────────{Colors.KRONOX_CYAN}║"""
        
        for cmd, desc in COMMANDS.items():
            help_text += f"""
    ║    {Colors.KRONOX_GREEN}{cmd:<18} {Colors.WHITE}{desc}{Colors.KRONOX_CYAN:<25} ║"""
        
        help_text += f"""
    ║                                                                ║
    ║    {Colors.KRONOX_PURPLE}🛰️  KRONOX-CHAT v3.0 - Secure Terminal Protocol{Colors.KRONOX_CYAN}   ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        print(help_text)

def main():
    if len(sys.argv) != 3:
        print(f"""
{Colors.KRONOX_CYAN}
    ╔════════════════════ MODO DE USO ═══════════════════════╗
    ║                                                        ║
    ║    {Colors.KRONOX_GREEN}USO: {Colors.WHITE}python client.py <host> <puerto>{Colors.KRONOX_CYAN:<15} ║
    ║                                                        ║
    ║    {Colors.KRONOX_YELLOW}EJEMPLOS:{Colors.KRONOX_CYAN:<40} ║
    ║      {Colors.WHITE}python client.py 192.168.1.10 8080{Colors.KRONOX_CYAN:<20} ║
    ║      {Colors.WHITE}python client.py localhost 8080{Colors.KRONOX_CYAN:<23} ║
    ║                                                        ║
    ║    {Colors.KRONOX_GREEN}O use los comandos globales KRONOX{Colors.KRONOX_CYAN:<20} ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
{Colors.RESET}
""")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    client = KronoxChatClient()
    client.connect(host, port)

if __name__ == "__main__":
    main()