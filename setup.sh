#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[38;5;196m"
echo "    ╔══════════════════════════════════════════════════╗"
echo "    ║                                                  ║"
echo "    ║           INSTALANDO KRONOX-CHAT v3.0            ║"
echo "    ║                                                  ║"
echo "    ╚══════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Actualizar sistema
echo -e "\033[38;5;208m📦 ACTUALIZANDO SISTEMA...\033[0m"
pkg update -y && pkg upgrade -y

# Instalar dependencias
echo -e "\033[38;5;226m🔧 INSTALANDO DEPENDENCIAS...\033[0m"
pkg install python -y
pkg install openssh -y

# Crear directorio KRONOX
echo -e "\033[38;5;46m📁 CREANDO DIRECTORIO KRONOX...\033[0m"
mkdir -p ~/kronox-chat

# Copiar archivos del sistema
cp server.py client.py config.py utils.py ~/kronox-chat/

# Hacer ejecutables
chmod +x ~/kronox-chat/*.py

# Crear comandos globales KRONOX
echo -e "\033[38;5;51m🔗 CREANDO COMANDOS GLOBALES...\033[0m"

# Comando: kronox-start
cat > ~/../usr/bin/kronox-start << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/kronox-chat
python server.py
EOF

# Comando: kronox-join
cat > ~/../usr/bin/kronox-join << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/kronox-chat
if [ $# -eq 2 ]; then
    python client.py $1 $2
else
    echo -e "\033[91mUSO: kronox-join <host> <puerto>"
    echo "EJEMPLO: kronox-join 192.168.1.10 8080"
    echo -e "EJEMPLO: kronox-join localhost 8080\033[0m"
fi
EOF

# Comando: kronox-info
cat > ~/../usr/bin/kronox-info << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo -e "\033[38;5;51m"
echo "    ╔════════════════════ KRONOX-CHAT v3.0 ════════════════════╗"
echo "    ║                                                          ║"
echo "    ║  🛰️   SISTEMA DE COMUNICACIONES TERMINAL                 ║"
echo "    ║                                                          ║"
echo "    ║  📡 COMANDOS DISPONIBLES:                                ║"
echo "    ║     • kronox-start    - Iniciar servidor                 ║"
echo "    ║     • kronox-join     - Conectar a servidor              ║"
echo "    ║     • kronox-info     - Mostrar información              ║"
echo "    ║     • kronox-update   - Actualizar sistema               ║"
echo "    ║                                                          ║"
echo "    ║  🔒 Protocolo Seguro de Comunicaciones Terminal          ║"
echo "    ║                                                          ║"
echo "    ╚══════════════════════════════════════════════════════════╝"
echo -e "\033[0m"
EOF

# Comando: kronox-update
cat > ~/../usr/bin/kronox-update << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/kronox-chat
echo -e "\033[38;5;208m🔄 ACTUALIZANDO KRONOX-CHAT...\033[0m"
if [ -d ".git" ]; then
    git pull
    echo -e "\033[38;5;46m✅ SISTEMA ACTUALIZADO\033[0m"
else
    echo -e "\033[93m⚠️  Actualización manual requerida\033[0m"
fi
EOF

# Hacer ejecutables los comandos
chmod +x ~/../usr/bin/kronox-*

echo -e "\033[38;5;46m"
echo "    ╔════════════════════ INSTALACIÓN COMPLETADA ═══════════════════╗"
echo "    ║                                                              ║"
echo "    ║  ✅ KRONOX-CHAT v3.0 INSTALADO CORRECTAMENTE                  ║"
echo "    ║                                                              ║"
echo "    ║  🚀 COMANDOS DISPONIBLES:                                    ║"
echo "    ║     📡 kronox-start    - Iniciar servidor                    ║"
echo "    ║     👥 kronox-join     - Conectar a servidor                 ║"
echo "    ║     🔧 kronox-info     - Mostrar información                 ║"
echo "    ║     🔄 kronox-update   - Actualizar sistema                  ║"
echo "    ║                                                              ║"
echo "    ║  💡 INICIO RÁPIDO:                                           ║"
echo "    ║     1. kronox-start         (en el servidor)                 ║"
echo "    ║     2. kronox-join <ip> 8080 (en clientes)                   ║"
echo "    ║                                                              ║"
echo "    ║  🌐 OBTENER IP: ifconfig                                     ║"
echo "    ║                                                              ║"
echo "    ╚══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"