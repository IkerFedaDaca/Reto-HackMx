from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

# Cargar credenciales
load_dotenv()

# Configuración de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener chromedriver en tu PATH
driver.get(httpswww.facebook.com)

# Iniciar sesión en Facebook
email_input = driver.find_element(By.ID, email)
password_input = driver.find_element(By.ID, pass)

email_input.send_keys(os.getenv(FACEBOOK_USER))
password_input.send_keys(os.getenv(FACEBOOK_PASS))
password_input.send_keys(Keys.RETURN)

time.sleep(5)  # Esperar a que cargue la página

# Aquí puedes agregar la lógica para verificar mensajes o notificaciones
# Por ejemplo, puedes ir a la sección de notificaciones y buscar palabras sospechosas.

# Cerrar sesión y el navegador
driver.quit()
