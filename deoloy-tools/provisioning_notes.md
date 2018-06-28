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
SITENAME\
     database\
     source\
     static\
     virtualenv\
     
######делаем:

1. cd ~/nginx/sites/SITENAME/source 
1. python3.6 -m venv ../virtualenv/ 
1. git clone https://github.com/ivc-inform/selenium-tests.git ~/nginx/sites/SITENAME/source/
1. source ../virtualenv/bin/activate
1. pip install --upgrade pip
1. source ../virtualenv/bin/activate
1. pip install -r requirements.txt   
1. python manage.py migrate
1. создать файл в каталоге /etc/nginx/sites-available с именем SITENAME из файла nginx-site-avalabel.conf заменив в нем SITENAME на настоящее имя
1. сделать ссылку sudo ln -s /etc/nginx/sites-available/SITENAME /etc/nginx/sites-enabled/SITENAME

####Конфигурация виртуальног узла Nginx   
* см nginx-site-avalabel.conf
* заменить SITENAME на доменное имя сайта
    