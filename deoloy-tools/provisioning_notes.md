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
2. python3.6 -m venv ../virtualenv/ 
3. git clone https://github.com/ivc-inform/selenium-tests.git

####Конфигурация виртуальног узла Nginx   
* см nginx-site-avalabel.conf
* заменить SITENAME на доменное имя сайта
    