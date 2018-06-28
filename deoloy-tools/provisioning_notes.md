Обеспечение работы нового сайта
===============================

##Необходимые пакеты
* nginx
* python 3.6
* virtualenv + pip
* Git

####Обновление пакетов 
#####для Ubuntu
    * sudo add-apt-repository ppa:fkrull/deadsnakes
    * sudo apt update
    * sudo apt install nginx git python3.6 python3.6-venv git

####Развертывание структуры файлов
/home/nginx/sites\
site_url\
     database\
     source\
     static\
     virtualenv\
     
######делаем:

1. cd ~/nginx/sites/site_url/source 
1. python3.6 -m venv ../virtualenv/ 
1. git clone https://github.com/ivc-inform/selenium-tests.git ~/nginx/sites/192.168.0.104/source/
1. source ../virtualenv/bin/activate
1. pip install --upgrade pip
1. source ../virtualenv/bin/activate
1. pip install -r requirements.txt   
1. python manage.py migrate

####Конфигурация виртуальног узла Nginx   
* см nginx-site-avalabel.conf
* заменить SITENAME на доменное имя сайта
    