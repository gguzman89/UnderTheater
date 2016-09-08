# Como instalar el entorno
## Requerimientos
* Python 2.7.6
* Django 1.10
* pip
* virtualenv
* Mysql

### Instalar python
~~~
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
cd ~/Downloads/
wget http://python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar -xvf Python-2.7.6.tgz
cd Python-2.7.6
./configure
make
sudo checkinstall
~~~
### Instalar Pip
~~~
apt-get -y install python-pip
~~~
### Instalar MySql
~~~
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo mysql_install_db
~~~
Para mas info ir a  [link](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-14-04)

En mysql crear un base de datos con nombre  "underTheater"
~~~
mysql -u root -p
>> CREATE DATABASE underTheater;
~~~
### Instalar VirtualEnv
~~~
 [sudo] pip install virtualenv
~~~
 
 ## Configurar el entorno
 
 1- clonar el repo con 
 ~~~
 git clone https://github.com/javierperini/UnderTheater.git
 ~~~
 2- Crear un virtualenv (es una maquina virtual para instalar las dependencias que son necesarias para el proyecto, no contaminas tu maquina con dependencias de mas).
 ~~~
 cd underTheater/
 virtualenv underTheaterWS
 ~~~
 Una vez hecho esto se tuvieron que haber creado carpetas /bin/ /lib/ /local/ /include/. 
 
 3- Paso siguiente ejecutar  
 ~~~
 cd underTheaterWS/
# Activa virtualenv
source bin/activate
# Instala dependencias
pip install -r requirements.txt

# Aplica migraciones de base de datos
./manage.py loaddata all.json
./manage.py migrate

# Da de alta el servidor
./manage runserver

# Aclaracion para salir de virtualenv
deactivate
 ~~~

  
