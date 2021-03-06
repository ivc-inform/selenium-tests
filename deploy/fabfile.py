import os
import random

from fabric.api import env
from fabric.contrib.files import exists, sed, append
from fabric.operations import run, local, sudo

REPO_URL = "https://github.com/ivc-inform/selenium-tests.git"


# fab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.100 deploy
# fab -u nginx -p nginx --sudo-password=nginx -H dev.db-support.ru deploy:81
# fab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.104 reDeploy
# fab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.100 makeService
# fab -u uandrew -p nginx --sudo-password=nginx -dev.db-support.ru makeService:81

def deploy(port_servise=80):
    siteName = env.host
    siteFolder = f"/home/{env.user}/sites/{siteName}"
    sourceFolder = f"{siteFolder}/source"

    sudo("apt install -y apache2-utils")
    sudo("add-apt-repository --yes ppa:fkrull/deadsnakes")
    sudo("apt update")
    sudo("apt dist-upgrade -y")
    sudo("apt install -y nginx git python3.6 python3.6-venv git")

    deployProcs(siteFolder, siteName, sourceFolder)
    serviceProcs(siteName, sourceFolder, env.user, port_servise)


def deployProcs(siteFolder, siteName, sourceFolder):
    createDirectoryStructure(siteFolder)
    getSources(sourceFolder)
    updateSetting(sourceFolder, siteName)
    updateVirtualEnv(sourceFolder)
    updateDatabase(sourceFolder)
    updateStatic(sourceFolder)


def reDeploy():
    siteName = env.host
    siteFolder = f"/home/{env.user}/sites/{siteName}"
    sourceFolder = f"{siteFolder}/source"

    deployProcs(siteFolder, siteName, sourceFolder)
    sudo(f"systemctl restart {siteName}")
    sudo(f"systemctl status {siteName}")


def createDirectoryStructure(siteFolder):
    for subfolder in ("database", "source", "static", "virtualenv"):
        run(f"mkdir -p {siteFolder}/{subfolder}")


def getSources(sourceFolder):
    if exists(f"{sourceFolder}/.git"):
        run(f"cd {sourceFolder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {sourceFolder}")

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {sourceFolder} && git reset --hard {current_commit}")


def updateSetting(sourceFolder, siteName):
    settingPath = f"{sourceFolder}/project/settings.py"
    if not exists(settingPath):
        raise Exception(f"File: {secretKeyFile} not exists.")
    sed(settingPath, "DEBUG = True", "DEBUG = False")
    sed(settingPath, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{siteName}"]')

    secretKeyFile = f"{sourceFolder}/project/secret_key.py"
    if not exists(secretKeyFile):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secretKeyFile, f'SECRET_KEY="{key}"')
    append(settingPath, '\nfrom .secret_key import SECRET_KEY')


def updateVirtualEnv(sourceFolder):
    virtualEnvFolder = f"{sourceFolder}/../virtualenv"
    if not exists(f"{virtualEnvFolder}/bin/pip"):
        run(f"python3.6 -m venv {virtualEnvFolder}")
    run(f"{virtualEnvFolder}/bin/pip install --upgrade pip")
    run(f"{virtualEnvFolder}/bin/pip install -r {sourceFolder}/requirements.txt")


def updateDatabase(sourceFolder):
    run(f"cd {sourceFolder} && ../virtualenv/bin/python3.6 manage.py migrate --noinput")


def updateStatic(sourceFolder):
    run(f"cd {sourceFolder} && ../virtualenv/bin/python3.6 manage.py collectstatic --noinput")


def makeService(port_servise=80):
    siteName = env.host
    siteFolder = f"/home/{env.user}/sites/{siteName}"
    sourceFolder = f"{siteFolder}/source"

    serviceProcs(siteName, sourceFolder, env.user, port_servise)


def restartService(port_servise=80):
    siteName = env.host
    _restartService(siteName)


def _restartService(siteName):
    sudo("systemctl daemon-reload")
    sudo(f"systemctl enable {siteName}")
    sudo(f"systemctl restart {siteName}")
    sudo(f"systemctl status {siteName}")


def serviceProcs(siteName, sourceFolder, username, port=80):
    sitesAvailableCfg = f"/etc/nginx/sites-available/{siteName}"
    sudo(f"cp {sourceFolder}/deploy-tools/nginx-site-avalabel.conf {sitesAvailableCfg}")
    sed(sitesAvailableCfg, "SITENAME", siteName, use_sudo=True)
    sed(sitesAvailableCfg, "PORT", str(port), use_sudo=True)
    sed(sitesAvailableCfg, "USERNAME", username, use_sudo=True)
    if not exists(f"/etc/nginx/sites-enabled/{siteName}"):
        sudo(f"ln -s /etc/nginx/sites-available/{siteName} /etc/nginx/sites-enabled/{siteName}")
    if exists(f"/etc/nginx/sites-enabled/default"):
        sudo("rm /etc/nginx/sites-enabled/default")
        sudo("systemctl reload nginx")
    servisePath = f"/etc/systemd/system/{siteName}.service"
    sudo(f"cp {sourceFolder}/deploy-tools/gunicorn-SITENAME.service {servisePath}")
    sed(servisePath, "SITENAME", siteName, use_sudo=True)
    sed(servisePath, "SMTP_SECRET", "Uandrew1965", use_sudo=True)
    sed(servisePath, "SECRET", "mt30718tm", use_sudo=True)
    sed(servisePath, "USERNAME", username, use_sudo=True)
    _restartService(siteName)


if __name__ == "__main__":
    os.chdir("")
