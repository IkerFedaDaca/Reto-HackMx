import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def send_test_email():
    remitente = os.getenv("USER")  # Correo electrónico del remitente
    password = os.getenv("PASS")    # Contraseña de aplicación del remitente
    destinatario = "destinatario@ejemplo.com"  # Reemplaza con el correo del destinatario

    # Configurar el contenido del correo
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Alerta de Seguridad en tu Red"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    # Cuerpo del correo
    body = """
    <html>
      <body>
        <h2>Hola, hemos detectado actividades sospechosas en tu red.</h2>
        <p>Por favor, revisa la siguiente información sobre los riesgos detectados:</p>
        <ul>
          <li>Actividad inusual por parte de un usuario</li>
          <li>Muchas solicitudes a páginas no protegidas</li>
          <li>Te llegó un mensaje al messenger con un idioma que no es el tuyo</li>
        </ul>
        <p>Haz clic en el botón a continuación para obtener más información:</p>
        <a href="https://github.com/IkerFedaDaca/Reto-HackMx" style="text-decoration: none;">
          <button style="padding: 10px 20px; color: white; background-color: #4CAF50; border: none; border-radius: 5px;">
            Más información
          </button>
        </a>
      </body>
    </html>
    """

    # Adjuntar el cuerpo HTML
    mensaje.attach(MIMEText(body, "html"))

    # Conectar al servidor SMTP de Gmail y enviar el correo
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Conexión segura
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, mensaje.as_string())
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ejecutar la función para enviar el correo de prueba
send_test_email()
