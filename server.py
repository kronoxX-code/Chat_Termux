# server.py
import socket
import threading
import time
import random
from config import SERVER_CONFIG, Colors, ROOMS
from utils import format_time, print_kronox_banner, get_user_color

class KronoxChatServer:
    def __init__(self):
        self.host = SERVER_CONFIG['host']
        self.port = SERVER_CONFIG['port']
        self.clients = []
        self.nicknames = []
        self.user_data = {}
        self.rooms = {room: [] for room in ROOMS.keys()}
        self.server_start_time = time.time()
        self.message_count = 0
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(SERVER_CONFIG['max_clients'])
        
        print_kronox_banner()
        print(f"{Colors.KRONOX_GREEN}🚀 INICIANDO SERVIDOR KRONOX-CHAT...{Colors.RESET}")
        print(f"{Colors.KRONOX_CYAN}📍 ENDPOINT: {self.host}:{self.port}{Colors.RESET}")
        print(f"{Colors.KRONOX_YELLOW}🕐 SERVER ID: KRONOX-{int(time.time())}{Colors.RESET}")
        print(f"{Colors.KRONOX_PURPLE}📡 ESCUCHANDO CONEXIONES...{Colors.RESET}\n")
        
        print(f"{Colors.KRONOX_GREEN}SALAS DISPONIBLES:{Colors.RESET}")
        for room, desc in ROOMS.items():
            print(f"  {Colors.KRONOX_CYAN}• {room}: {desc}{Colors.RESET}")
        print()
        
        try:
            while True:
                client, address = self.server.accept()
                threading.Thread(target=self.handle_client, args=(client,)).start()
        except KeyboardInterrupt:
            print(f"\n{Colors.KRONOX_RED}🛑 DETENIENDO SERVIDOR KRONOX...{Colors.RESET}")
            self.shutdown()
    
    def handle_client(self, client):
        try:
            # Fase de autenticación
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            # Verificar y hacer único el nickname
            original_nickname = nickname
            counter = 1
            while nickname in self.nicknames:
                nickname = f"{original_nickname}_{counter}"
                counter += 1
            
            # Registrar usuario
            user_id = f"USER-{random.randint(1000, 9999)}"
            user_color = get_user_color(nickname)
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            self.user_data[client] = {
                'nickname': nickname,
                'user_id': user_id,
                'join_time': time.time(),
                'room': 'general',
                'color': user_color,
                'message_count': 0
            }
            self.rooms['general'].append(client)
            
            # Mensaje de bienvenida KRONOX
            welcome_msg = f"""
{Colors.KRONOX_GREEN}{Colors.BOLD}
    ╔══════════════════════════ BIENVENIDO ══════════════════════════╗
    ║                                                                ║
    ║    {Colors.KRONOX_CYAN}✅ IDENTIFICACIÓN: {nickname:<30} {Colors.KRONOX_GREEN}║
    ║    {Colors.KRONOX_YELLOW}🆔 CÓDIGO USUARIO: {user_id:<28} {Colors.KRONOX_GREEN}║
    ║    {Colors.KRONOX_BLUE}📍 SALA ASIGNADA: General{Colors.KRONOX_GREEN:<30} ║
    ║    {Colors.KRONOX_PURPLE}👥 USUARIOS CONECTADOS: {len(self.clients):<23} {Colors.KRONOX_GREEN}║
    ║                                                                ║
    ║    {Colors.WHITE}Escribe {Colors.KRONOX_CYAN}/help{Colors.WHITE} para ver comandos del sistema{Colors.KRONOX_GREEN}     ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
            client.send(welcome_msg.encode('utf-8'))
            
            # Notificar ingreso a la sala
            join_msg = f"{Colors.KRONOX_GREEN}🟢 SISTEMA: {Colors.KRONOX_CYAN}{nickname} {Colors.KRONOX_GREEN}ha ingresado al canal ({len(self.clients)} usuarios activos){Colors.RESET}"
            self.broadcast_to_room(join_msg, client, 'general')
            
            print(f"{Colors.KRONOX_GREEN}✅ NUEVA CONEXIÓN: {nickname} ({user_id}) - Total: {len(self.clients)} usuarios{Colors.RESET}")
            
            # Loop principal del cliente
            while True:
                message = client.recv(1024).decode('utf-8')
                
                if message.startswith('/'):
                    self.handle_client_command(client, message)
                else:
                    self.handle_normal_message(client, message)
                    
        except Exception as e:
            self.remove_client(client)
    
    def handle_normal_message(self, client, message):
        user_info = self.user_data[client]
        user_info['message_count'] += 1
        self.message_count += 1
        
        # Formatear mensaje con estilo KRONOX
        timestamp = format_time()
        user_color = getattr(Colors, user_info['color'])
        room = user_info['room']
        
        formatted_msg = f"""
{Colors.KRONOX_BLUE}    ┌────────────────────────────────────────────────────────────────┐
    │ {Colors.GRAY}🕐 {timestamp} {user_color}{user_info['nickname']:<15} {Colors.KRONOX_YELLOW}({room}){Colors.KRONOX_BLUE}                     │
    │ {Colors.WHITE}{message:<60} {Colors.KRONOX_BLUE}│
    └────────────────────────────────────────────────────────────────┘{Colors.RESET}"""
        
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
            error_msg = f"{Colors.KRONOX_RED}❌ COMANDO NO RECONOCIDO: Use {Colors.KRONOX_CYAN}/help{Colors.KRONOX_RED} para ayuda{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def send_users_list(self, client):
        users_msg = f"""
{Colors.KRONOX_CYAN}{Colors.BOLD}
    ╔══════════════════════ USUARIOS CONECTADOS ═════════════════════╗
    ║                                                                ║
    ║    {Colors.KRONOX_GREEN}👥 TOTAL: {len(self.clients)} usuarios{Colors.KRONOX_CYAN:<45} ║
    ║                                                                ║{Colors.RESET}"""
        
        for i, user_client in enumerate(self.clients):
            user_data = self.user_data[user_client]
            color = getattr(Colors, user_data['color'])
            users_msg += f"""
    ║    {color}🔹 {user_data['nickname']:<20} {Colors.GRAY}({user_data['room']}){Colors.KRONOX_CYAN:<25} ║"""
        
        users_msg += f"""
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        client.send(users_msg.encode('utf-8'))
    
    def send_private_message(self, client, target_nickname, message):
        sender_data = self.user_data[client]
        target_client = None
        
        for user_client, user_data in self.user_data.items():
            if user_data['nickname'] == target_nickname:
                target_client = user_client
                break
        
        if target_client:
            timestamp = format_time()
            pm_msg = f"""
{Colors.KRONOX_PURPLE}{Colors.BOLD}
    ╔════════════════════ MENSAJE PRIVADO ═══════════════════════╗
    ║                                                            ║
    ║    {Colors.KRONOX_CYAN}DE: {sender_data['nickname']:<15} → PARA: {target_nickname:<15} {Colors.KRONOX_PURPLE}║
    ║    {Colors.GRAY}🕐 {timestamp:<50} {Colors.KRONOX_PURPLE}║
    ║                                                            ║
    ║    {Colors.WHITE}{message:<58} {Colors.KRONOX_PURPLE}║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
            target_client.send(pm_msg.encode('utf-8'))
            client.send(pm_msg.encode('utf-8'))
        else:
            error_msg = f"{Colors.KRONOX_RED}❌ USUARIO NO ENCONTRADO: {target_nickname}{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def change_nickname(self, client, new_nickname):
        old_nickname = self.user_data[client]['nickname']
        
        if new_nickname not in self.nicknames:
            self.nicknames.remove(old_nickname)
            self.nicknames.append(new_nickname)
            self.user_data[client]['nickname'] = new_nickname
            
            change_msg = f"{Colors.KRONOX_YELLOW}🔄 SISTEMA: {old_nickname} cambió su identificación a {new_nickname}{Colors.RESET}"
            self.broadcast_to_room(change_msg, client, self.user_data[client]['room'])
        else:
            error_msg = f"{Colors.KRONOX_RED}❌ IDENTIFICACIÓN EN USO: {new_nickname}{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def change_room(self, client, new_room):
        if new_room in ROOMS:
            old_room = self.user_data[client]['room']
            
            # Remover de sala anterior
            if client in self.rooms[old_room]:
                self.rooms[old_room].remove(client)
                leave_msg = f"{Colors.KRONOX_GRAY}📤 {self.user_data[client]['nickname']} abandonó la sala{Colors.RESET}"
                self.broadcast_to_room(leave_msg, client, old_room)
            
            # Agregar a nueva sala
            self.rooms[new_room].append(client)
            self.user_data[client]['room'] = new_room
            
            join_msg = f"{Colors.KRONOX_GREEN}📥 {self.user_data[client]['nickname']} se unió a la sala{Colors.RESET}"
            self.broadcast_to_room(join_msg, client, new_room)
            
            room_msg = f"{Colors.KRONOX_CYAN}📍 SALA CAMBIADA: {old_room} → {new_room}{Colors.RESET}"
            client.send(room_msg.encode('utf-8'))
        else:
            error_msg = f"{Colors.KRONOX_RED}❌ SALA NO DISPONIBLE: {new_room}{Colors.RESET}"
            client.send(error_msg.encode('utf-8'))
    
    def send_system_info(self, client):
        uptime = time.time() - self.server_start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        
        info_msg = f"""
{Colors.KRONOX_CYAN}{Colors.BOLD}
    ╔════════════════════ INFORMACIÓN DEL SISTEMA ═══════════════════╗
    ║                                                                ║
    ║    {Colors.KRONOX_GREEN}🛰️  SISTEMA: KRONOX-CHAT v3.0{Colors.KRONOX_CYAN:<35} ║
    ║    {Colors.KRONOX_YELLOW}⏰ TIEMPO ACTIVO: {hours}h {minutes}m{Colors.KRONOX_CYAN:<32} ║
    ║    {Colors.KRONOX_BLUE}👥 USUARIOS: {len(self.clients)} conectados{Colors.KRONOX_CYAN:<35} ║
    ║    {Colors.KRONOX_PURPLE}💬 MENSAJES: {self.message_count} totales{Colors.KRONOX_CYAN:<34} ║
    ║    {Colors.KRONOX_GREEN}📡 SALAS: {len(ROOMS)} disponibles{Colors.KRONOX_CYAN:<35} ║
    ║                                                                ║
    ║    {Colors.WHITE}SALAS ACTIVAS:{Colors.KRONOX_CYAN:<44} ║"""
        
        for room, users in self.rooms.items():
            if users:
                info_msg += f"""
    ║      {Colors.KRONOX_YELLOW}• {room}: {len(users)} usuarios{Colors.KRONOX_CYAN:<38} ║"""
        
        info_msg += f"""
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
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
            
            leave_msg = f"{Colors.KRONOX_RED}🔴 SISTEMA: {nickname} abandonó la red ({len(self.clients)} usuarios restantes){Colors.RESET}"
            self.broadcast_to_room(leave_msg, client, room)
            
            print(f"{Colors.KRONOX_RED}❌ DESCONEXIÓN: {nickname} - Total: {len(self.clients)} usuarios{Colors.RESET}")
            
            del self.user_data[client]
            client.close()
    
    def shutdown(self):
        shutdown_msg = f"{Colors.KRONOX_RED}🛑 SERVIDOR KRONOX OFFLINE - Cerrando conexiones...{Colors.RESET}"
        for client in self.clients:
            try:
                client.send(shutdown_msg.encode('utf-8'))
                client.close()
            except:
                pass
        self.server.close()

if __name__ == "__main__":
    server = KronoxChatServer()
    server.start()