# config.py
class Colors:
    # Colores básicos optimizados
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Estilos
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Configuración del servidor
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 8080,
    'max_clients': 50,
    'buffer_size': 1024
}

# Comandos disponibles
COMMANDS = {
    '/help': 'Mostrar ayuda',
    '/users': 'Listar usuarios',
    '/pm': 'Mensaje privado',
    '/nick': 'Cambiar nickname',
    '/room': 'Cambiar sala',
    '/quit': 'Salir',
    '/info': 'Info del servidor'
}

# Emojis simples
EMOJIS = {
    ':)': '😊',
    ':(': '😢',
    ':D': '😃',
    ';)': '😉',
    '<3': '❤️',
    ':P': '😛'
}

# Salas disponibles
ROOMS = {
    'general': 'Sala Principal',
    'comandos': 'Comandos',
    'offtopic': 'Off Topic'
}
