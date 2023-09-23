# Modulos python
import os
import sys
import time
import pickle
import tempfile
# Modulos de terceros
from selenium.webdriver.common.by import By # buscar tipos de elementos
from selenium.webdriver.support.ui import WebDriverWait # para esperar elementos de selenium
from selenium.webdriver.support import expected_conditions as ec # indicar condiciones de selenium
# Modulos propios
from config import *
from Funciones.colores import *
from Funciones.iniciar_webdriver_uc import iniciar_webdriver

def cursor_arriba(n=1):
    """Sube el cursor de la teminal n lineas mas arriba"""
    print(f'\33[{n}A',end='')

class ChatGpt:
    def __init__(self,user,password):
        
        self.OPENAI_USER=user
        self.OPENAI_PASS=password
        self.COOKIES_FILE=f'{tempfile.gettempdir()}/openai.cookies'
        print(f'{Azul}Iniciando webdriver{Magenta}')
        self.driver=iniciar_webdriver(headless=False,pos="izquierda") # esperara 30 segundos
        self.wait=WebDriverWait(self.driver,30)
        login=self.login_openai()
        print()
        if not login:
            sys.exit(1)

    def login_openai(self):
        """ Realizara login en openai por cookies o desde cero() se guardan las cookies"""
        # LOGIN DESDE CERO
        print('LOGIN DESDE CERO')
        print('cargamos chatgpt')
        self.driver.get('https://chat.openai.com/')
        #click en el login
        cursor_arriba()
        print('click login')
        e=self.wait.until(ec.element_to_be_clickable((By.XPATH,"//div[text()='Log in']")))
        e.click()
        
        #introduciomos usuario
        cursor_arriba()
        print('introducimos usuario')
        e=self.wait.until(ec.element_to_be_clickable((By.ID,'username')))
        e.send_keys(self.OPENAI_USER)
        #click en el login
        cursor_arriba()
        print('click en continue')
        e=self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,"button[name='action]")))
        e.click()

        #introducimos la contrasenia
        cursor_arriba()
        print('introducimos contrasenia')
        e=self.wait.until(ec.element_to_be_clickable((By.ID,'password')))
        e.send_keys(self.OPENAI_PASS)
        #click en el continue
        cursor_arriba()
        print('click en continue')
        e=self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,"button[name='action]")))
        e.click()

        # comprobamos login
        login=self.comprobar_login()
        if login:
            #guardamos cookies
            pickle.dump(self.driver.get_cookies(),open(self.COOKIES_FILE,'wb'))
            print(f'Login desde cero: OK')
        else:
            print('Login desde cero: Fallido')

        return login
    
    def comprobar_login(self,tiempo=30):
        login=False
        while tiempo>0:
            #click en next
            try:
                e=self.driver.find_element(By.XPATH,"//div[text()='Next']")
                e.click()
            except:
                pass
            #click en done
            try:
                e=self.driver.find_element(By.XPATH,"//div[text()='Done']")
                e.click()
            except:
                pass
            #login correcto
            try:
                e=self.driver.find_element(By.CSS_SELECTOR,"textarea[tabindex='0']")
                e.click()
                login=True
                break
            except:
                pass
            #login incorrecto
            try:
                e=self.driver.find_element(By.ID,"username")
                break
            except:
                pass
            #sesion expirada las cookies
            try:
                e=self.driver.find_element(By.CSS_SELECTOR,"h3.text-lg")
                if "session has expired" in e.text:
                    cursor_arriba()
                    print("La session a expirado")
                    print()
                    break
            except:
                pass
            #pausa
            cursor_arriba()
            print('Comprobando login...')
            time.sleep(1)
            tiempo-=1

        return login


# MAIN
#if __name__=='__main__':
#    chatgpt=ChatGpt(OPENAI_USER,OPENAI_PASS) 
#    input("Pausa...")
#
