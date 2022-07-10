# DNS Updater
Guia de instalacion de Actualizador de DNS en Hostinger
Desarrollado en Python 3.9.2

1) Instale selenium y pyvirtualdisplay

2) Instale la libreria undetected-chromedriver, para hacerlo ejecute el siguiente comando dentro de la carpeta del paquete.

sudo python setup.py install

Nota: la libreria descarga la version de chromedriver para chromium 98, como yo necesitaba la 101 la modifique para que pise el chromedriver descargado con el de la 101. Linea 220 del archivo patcher de la libreria.

3) Asegurese de tener instalado chromium v101 (si no se puede esa version descargar la ultima version tanto de chromium como de chromedriver, a esta ultima copiarla y reemplazar chromedriver_101_OK)

4) De ser necesario, instalar los siguientes paquetes. Es probable que se necesiten para usarlo con visible=True

sudo apt-get install xffb
sudo apt-get install xserver-zhepyr

5) Recuerde modificar los valores de email y contraseña en el codigo. Sino no va a loguear y va a dar error.

6) Ya deberia funcionar python con undetected_chromedriver.

Nota: para hacerlo visible o invisible hay un flag en la funcion Display()
visible = False