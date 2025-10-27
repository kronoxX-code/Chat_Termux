#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[96m"
echo "┌────────────────────────────────────────┐"
echo "│         KRONOX-CHAT v3.0               │"
echo "└────────────────────────────────────────┘"
echo -e "\033[0m"

# Actualizar e instalar dependencias
pkg update -y
pkg install python -y

# Crear directorio
mkdir -p ~/kronox-chat

# Copiar archivos
cp server.py client.py config.py utils.py ~/kronox-chat/

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
    echo -e "\033[91mUso: kronox-join <host> <puerto>"
    echo "Ejemplo: kronox-join 192.168.1.10 8080"
    echo -e "Ejemplo: kronox-join localhost 8080\033[0m"
fi
EOF

# Hacer ejecutables
chmod +x ~/../usr/bin/kronox-*

echo -e "\033[92m"
echo "✅ Instalación completada!"
echo ""
echo "🚀 Comandos disponibles:"
echo "   kronox-start    - Iniciar servidor"
echo "   kronox-join     - Conectar a servidor"
echo ""
echo "💡 Uso rápido:"
echo "   1. kronox-start          (servidor)"
echo "   2. kronox-join IP 8080   (cliente)"
echo -e "\033[0m"
