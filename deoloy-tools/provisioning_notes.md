Развертывание сайта
===============================

##Первый раз:
###Выполняется из каталога deploy-tools
* fab -u USERNAME -p PASSWORD --sudo-password=SUDO_PASSWORD -H HOST deploy \
USERNAME, PASSWORD : пользователь и пароль того места, куда производится установка, например:
   * fab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.104 deploy
   
   
##При обновлении версии:
###Выполняется из каталога deploy-tools
* fab -u USERNAME -p PASSWORD --sudo-password=SUDO_PASSWORD -H HOST reDeploy \
USERNAME, PASSWORD : пользователь и пароль того места, куда производится установка, например:
   * fab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.104 reDeploy    

    