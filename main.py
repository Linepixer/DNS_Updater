#!/usr/bin/python
import os
import json
import requests
import socket
import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

version = "1.3"

def get_public_ip():
	return requests.get("https://ipinfo.io/json", verify = True).json()['ip']

def get_domain_destination_ip(domain):
	return socket.gethostbyname(domain)

def update_hostinger(public_ip):
	print("INFO >> Executing update")
	display = Display(visible=False, size=(1920, 1080))
	display.start()

	# Parametros iniciales del webdriver
	options = uc.ChromeOptions()
	options.add_argument("--disable-features=ChromeWhatsNewUI")

	print("INFO >> Starting browser")
	driver = uc.Chrome(options=options)
	driver.maximize_window()

	# Cargo la pagina
	print("INFO >> Loading page")
	driver.get('https://www.hostinger.com.ar/cpanel-login')
	
	# Ingreso los datos de login
	print("INFO >> Logging in")
	WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.NAME, "email")))
	email_input = driver.find_element(by=By.NAME, value="email")
	email_input.send_keys("your_email") # REEMPLAZAR CON EMAIL DE HOSTINGER
	WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.NAME, "password")))
	password_input = driver.find_element(by=By.NAME, value="password")
	password_input.send_keys("your_password", Keys.ENTER) #REEMPLAZAR CON CONTRASEÑA DE HOSTINGER
	
	# Redirecciono a la configuracion de dns
	WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "hpanel_tracking-home-manage_button")))
	print("INFO >> Loading DNS settings")
	driver.get('https://hpanel.hostinger.com/domain/linepixer.tech/dns')
	# Borro todas las configuraciones anteriores de dns
	WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "h-data-table_body")))
	driver.execute_script("window.scrollTo(0, 600)")
	sleep(2)
	print("INFO >> Eliminating previous configuration")
	while True:
		try:
			sleep(3)
			delete_button = driver.find_element(by=By.ID, value="hpanel_tracking-domain-dns-delete_button")
			delete_button.click()
		except:
			try:
				sleep(3)
				driver.find_element(by=By.ID, value="hpanel_tracking-domain-dns-delete_button")
				delete_button.click()
				continue
			except:
				print("INFO >> There are no more configurations to eliminate")
				break
	print("INFO >> Configuring main domain")
	# Ubico el boton "Agregar registro"
	add_record_button = driver.find_element(by=By.ID, value="hdomains_dns_create_record_add")
	# Creo el registro principal
	server_ip = driver.find_element(by=By.ID, value="hdomains_dns_create_record_pointsTo")
	server_ip.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
	server_ip.send_keys(public_ip)
	add_record_button.click()
	# Crea el registro WWW
	WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "hdomains_dns_create_record_add")))
	print("INFO >> Configuring WWW subdomain")
	subdomain_input = driver.find_element(by=By.ID, value="hdomains_dns_create_record_name")
	subdomain_input.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
	subdomain_input.send_keys("www")
	add_record_button.click()
	sleep(3)
	# Cierro el webdriver
	driver.close()
	display.stop()
	print("SUCCESS >> Updated DNS")

if __name__ == '__main__':
	os.system("mkdir ~/.local/share/undetected_chromedriver/")
	print("INFO >> Starting DNS Updater v{}...".format(version))
	copy_command = "cp" + " " + os.getcwd() + "/" + "chromedriver_101_OK" + " " + "~/.local/share/undetected_chromedriver/chromedriver_101_OK"
	os.system(copy_command)
	while True:
		try:
			# Obtengo IPs
			public_ip = get_public_ip()
			domain_destination_ip = get_domain_destination_ip("linepixer.tech") #REEMPLAZAR linepixer.tech POR EL DOMINIO QUE CORRESPONDA
			# Si las IPs son distintas entonces actualizo hostinger
			# public_ip = "8.8.8.8" #PARA TESTING
			# domain_destination_ip = "4.4.4.4" #PARA TESTING
			if public_ip != domain_destination_ip:
				update_hostinger(public_ip)
		except Exception as e:
			print(e)
			# Si algo falla aparecera este mensaje
			print("ERROR >> Failed to perform the operation")
		# Entre bucles espero 5 minutos
		sleep(300)
