from scapy.all import sniff
from collections import defaultdict
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Configuraciones
http_requests = defaultdict(int)
https_requests = defaultdict(int)
ssh_attempts = defaultdict(int)
ping_requests = defaultdict(int)
THRESHOLD = 10  # Número de paquetes para considerar actividad sospechosa

# Función para enviar alertas por correo
def send_alert_email(subject, body):
    load_dotenv()  # Cargar variables de entorno
    remitente = os.getenv('USER')
    password = os.getenv('PASS')

    # Configurar el mensaje de correo
    message = MIMEMultipart()
    message['From'] = remitente
    message['To'] = 'alanghescuela00@gmail.com'
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Conectar al servidor SMTP y enviar el mensaje
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Conexión segura
        server.login(remitente, password)  # Autenticación
        server.send_message(message)

# Función para analizar paquetes
def packet_analyzer(packet):
    global http_requests, https_requests, ssh_attempts, ping_requests

    # Análisis de Ping
    if packet.haslayer('ICMP'):
        src_ip = packet['IP'].src
        ping_requests[src_ip] += 1
        if ping_requests[src_ip] > THRESHOLD:
            body = f"Sospecha de ataque de ping desde {src_ip} con {ping_requests[src_ip]} pings."
            send_alert_email("Alerta de Ping DDoS Detectada", body)
            ping_requests[src_ip] = 0  # Reiniciar conteo

    # Análisis de HTTP
    elif packet.haslayer('TCP') and packet['TCP'].dport == 80:
        src_ip = packet['IP'].src
        http_requests[src_ip] += 1
        if http_requests[src_ip] > THRESHOLD:
            body = f"Tráfico HTTP sospechoso desde {src_ip} con {http_requests[src_ip]} solicitudes."
            send_alert_email("Alerta de Tráfico HTTP No Seguro", body)
            http_requests[src_ip] = 0  # Reiniciar conteo

    # Análisis de HTTPS
    elif packet.haslayer('TCP') and packet['TCP'].dport == 443:
        src_ip = packet['IP'].src
        https_requests[src_ip] += 1
        if https_requests[src_ip] > THRESHOLD:
            body = f"Tráfico HTTPS alto desde {src_ip} con {https_requests[src_ip]} solicitudes."
            send_alert_email("Alerta de Tráfico HTTPS Alto", body)
            https_requests[src_ip] = 0  # Reiniciar conteo

    # Análisis de SSH
    elif packet.haslayer('TCP') and packet['TCP'].dport == 22:
        src_ip = packet['IP'].src
        ssh_attempts[src_ip] += 1
        if ssh_attempts[src_ip] > THRESHOLD:
            body = f"Intentos de conexión SSH sospechosos desde {src_ip} con {ssh_attempts[src_ip]} intentos."
            send_alert_email("Alerta de Fuerza Bruta en SSH", body)
            ssh_attempts[src_ip] = 0  # Reiniciar conteo

# Iniciar monitoreo en la red
print("Iniciando monitoreo de red...")
sniff(filter="tcp port 80 or tcp port 443 or tcp port 22 or icmp", prn=packet_analyzer)
