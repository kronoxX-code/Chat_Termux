# config.py
class Colors:
    # Colores KRONOX
    KRONOX_RED = '\033[38;5;196m'
    KRONOX_ORANGE = '\033[38;5;208m'
    KRONOX_YELLOW = '\033[38;5;226m'
    KRONOX_GREEN = '\033[38;5;46m'
    KRONOX_CYAN = '\033[38;5;51m'
    KRONOX_BLUE = '\033[38;5;33m'
    KRONOX_PURPLE = '\033[38;5;93m'
    KRONOX_PINK = '\033[38;5;201m'
    
    # Colores básicos
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
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Configuración del servidor
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 8080,
    'max_clients': 100,
    'buffer_size': 2048,
    'timeout': 60
}

# Comandos KRONOX
COMMANDS = {
    '/help': 'Mostrar ayuda del sistema',
    '/users': 'Listar usuarios conectados',
    '/pm': 'Mensaje privado (/pm usuario mensaje)',
    '/clear': 'Limpiar terminal',
    '/quit': 'Salir del sistema',
    '/color': 'Cambiar color de usuario',
    '/nick': 'Cambiar identificación',
    '/room': 'Cambiar sala de operaciones',
    '/emoji': 'Mostrar códigos emoji',
    '/info': 'Estado del sistema KRONOX',
    '/time': 'Mostrar tiempo del servidor',
    '/admin': 'Comandos administrativos'
}

# Emojis KRONOX
EMOJIS = {
    ':)': '😊',
    ':(': '😢',
    ':D': '😃',
    ';)': '😉',
    ':P': '😛',
    ':O': '😮',
    '<3': '❤️',
    ':/': '😕',
    ':|': '😐',
    ':*': '😘',
    '+1': '👍',
    '-1': '👎',
    '!!': '⚠️',
    '...': '💭',
    '->': '➡️',
    '<-': '⬅️'
}

# Salas disponibles
ROOMS = {
    'general': 'Sala Principal',
    'comandos': 'Comandos y Control',
    'tecnica': 'Soporte Técnico',
    'seguridad': 'Operaciones Seguras',
    'offtopic': 'Zona Libre'
}