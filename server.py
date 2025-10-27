# server.py
import socket
import threading
import time
import random
from config import SERVER_CONFIG, Colors, ROOMS
from utils import format_time, get_user_color

class KronoxChatServer:
    def __init__(self):
        self.host = SERVER_CONFIG['host']
        self.port = SERVER_CONFIG['port']
        self.clients = []
        self.nicknames = []
        self.user_data = {}
        self.rooms = {room: [] for room in ROOMS.keys()}
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(SERVER_CONFIG['max_clients'])
        
        print(f"{Colors.CYAN}╔════════════════════════════════════════╗")
        print(f"║           KRONOX-CHAT SERVER           ║")
        print(f"║     Puerto: {self.port} - Esperando conexiones   ║")
        print(f"╚════════════════════════════════════════╝{Colors.RESET}")
        
        try:
            while True:
                client, address = self.server.accept()
                threading.Thread(target=self.handle_client, args=(client,)).start()
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}⏹️  Servidor detenido{Colors.RESET}")
            self.shutdown()
    
    def handle_client(self, client):
        try:
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            # Hacer nickname único
            original_nickname = nickname
            counter = 1
            while nickname in self.nicknames:
                nickname = f"{original_nickname}_{counter}"
                counter += 1
            
            # Registrar usuario
            user_color = get_user_color(nickname)
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            self.user_data[client] = {
                'nickname': nickname,
                'room': 'general',
                'color': user_color
            }
            self.rooms['general'].append(client)
            
            # Mensaje de bienvenida simple
            welcome_msg = f"{Colors.GREEN}✅ Conectado como: {nickname}{Colors.RESET}"
            client.send(welcome_msg.encode('utf-8'))
            
            # Notificar a otros
            join_msg = f"{Colors.CYAN}👤 {nickname} se unió al chat ({len(self.clients)} usuarios){Colors.RESET}"
            self.broadcast_to_room(join_msg, client, 'general')
            
            print(f"{Colors.GREEN}✅ {nickname} conectado - Total: {len(self.clients)}{Colors.RESET}")
            
            # Loop principal
            while True:
                message = client.recv(1024).decode('utf-8')
                
                if message.startswith('/'):
                    self.handle_client_command(client, message)
                else:
                    self.handle_normal_message(client, message)
                    
        except:
            self.remove_client(client)
    
    def handle_normal_message(self, client, message):
        user_info = self.user_data[client]
        timestamp = format_time()
        user_color = getattr(Colors, user_info['color'])
        room = user_info['room']
        
        formatted_msg = f"{Colors.GRAY}[{timestamp}]{Colors.RESET} {user_color}{user_info['nickname']}{Colors.RESET}: {message}"
        self.broadcast_to_room(formatted_msg, client, room)
    
    def handle_client_command(self, client, message):
        parts = message.split(' ')
        command = parts[0].lower()
        user_info = self.user_data[client]
        
        if command == '/users':
            self.send_users_list(client)
        elif command == '/pm' and len(parts) >= 3:
            self.send_private_message(client, parts[1], ' '.join(parts[2:]))
        elif command == '/nick' and len(parts) >= 2:
            self.change_nickname(client, parts[1])
        elif command == '/room' and len(parts) >= 2:
            self.change_room(client, parts[1])
        elif command == '/info':
            self.send_system_info(client)
        elif command == '/quit':
            self.remove_client(client)
        else:
            error_msg = f"{Colors.RED}❌ Comando no reconocido. Usa /help{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def send_users_list(self, client):
        users_msg = f"{Colors.CYAN}👥 Usuarios ({len(self.clients)}):{Colors.RESET}\n"
        for user_client in self.clients:
            user_data = self.user_data[user_client]
            users_msg += f"  {user_data['nickname']} ({user_data['room']})\n"
        client.send(users_msg.encode('utf-8'))
    
    def send_private_message(self, client, target_nickname, message):
        sender_data = self.user_data[client]
        target_client = None
        
        for user_client, user_data in self.user_data.items():
            if user_data['nickname'] == target_nickname:
                target_client = user_client
                break
        
        if target_client:
            pm_msg = f"{Colors.MAGENTA}📨 {sender_data['nickname']} → {target_nickname}: {message}{Colors.RESET}"
            target_client.send(pm_msg.encode('utf-8'))
            client.send(pm_msg.encode('utf-8'))
        else:
            error_msg = f"{Colors.RED}❌ Usuario no encontrado: {target_nickname}{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def change_nickname(self, client, new_nickname):
        old_nickname = self.user_data[client]['nickname']
        
        if new_nickname not in self.nicknames:
            self.nicknames.remove(old_nickname)
            self.nicknames.append(new_nickname)
            self.user_data[client]['nickname'] = new_nickname
            
            change_msg = f"{Colors.YELLOW}🔄 {old_nickname} ahora es {new_nickname}{Colors.RESET}"
            self.broadcast_to_room(change_msg, client, self.user_data[client]['room'])
        else:
            error_msg = f"{Colors.RED}❌ Nickname en uso: {new_nickname}{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def change_room(self, client, new_room):
        if new_room in ROOMS:
            old_room = self.user_data[client]['room']
            
            # Remover de sala anterior
            if client in self.rooms[old_room]:
                self.rooms[old_room].remove(client)
                leave_msg = f"{Colors.GRAY}📤 {self.user_data[client]['nickname']} salió{Colors.RESET}"
                self.broadcast_to_room(leave_msg, client, old_room)
            
            # Agregar a nueva sala
            self.rooms[new_room].append(client)
            self.user_data[client]['room'] = new_room
            
            join_msg = f"{Colors.GREEN}📥 {self.user_data[client]['nickname']} se unió{Colors.RESET}"
            self.broadcast_to_room(join_msg, client, new_room)
            
            room_msg = f"{Colors.CYAN}📍 Sala cambiada: {old_room} → {new_room}{Colors.RESET}"
            client.send(room_msg.encode('utf-8'))
        else:
            error_msg = f"{Colors.RED}❌ Sala no disponible: {new_room}{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def send_system_info(self, client):
        info_msg = f"""{Colors.CYAN}
╔════════════════════════════════════════╗
║             KRONOX-CHAT v3.0           ║
║                                        ║
║  👥 Usuarios: {len(self.clients)} conectados          ║
║  📡 Salas: {len(ROOMS)} disponibles            ║
║  🛰️  Puerto: {self.port}                    ║
║                                        ║
╚════════════════════════════════════════╝
{Colors.RESET}"""
        client.send(info_msg.encode('utf-8'))
    
    def broadcast_to_room(self, message, sender_client, room):
        for client in self.rooms[room]:
            if client != sender_client:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)
    
    def remove_client(self, client):
        if client in self.clients:
            user_data = self.user_data[client]
            nickname = user_data['nickname']
            room = user_data['room']
            
            self.clients.remove(client)
            self.nicknames.remove(nickname)
            
            if room in self.rooms and client in self.rooms[room]:
                self.rooms[room].remove(client)
            
            leave_msg = f"{Colors.RED}👋 {nickname} abandonó el chat ({len(self.clients)} usuarios){Colors.RESET}"
            self.broadcast_to_room(leave_msg, client, room)
            
            print(f"{Colors.RED}❌ {nickname} desconectado - Total: {len(self.clients)}{Colors.RESET}")
            
            del self.user_data[client]
            client.close()
    
    def shutdown(self):
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.server.close()

if __name__ == "__main__":
    server = KronoxChatServer()
    server.start()
