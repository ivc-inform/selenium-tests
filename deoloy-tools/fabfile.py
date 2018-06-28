import random

from fabric.api import env
from fabric.contrib.files import exists, sed, append
from fabric.operations import run, local, sudo

REPO_URL = "https://github.com/ivc-inform/selenium-tests.git"


# fab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.104 deploy

def deploy():
    siteName = env.host
    siteFolder = f"/home/{env.user}/nginx/sites/{siteName}"
    sourceFolder = f"{siteFolder}/source"

    sudo("apt install apache2-utils")
    sudo("add-apt-repository --yes ppa:fkrull/deadsnakes")
    sudo("apt update")
    sudo("apt install -y nginx git python3.6 python3.6-venv git")

    createDirectoryStructure(siteFolder)
    getSources(sourceFolder)
    updateSetting(sourceFolder, siteName)
    updateVirtualEnv(sourceFolder)
    updateDatabase(sourceFolder)
    updateStatic(sourceFolder)


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
    run(f"{virtualEnvFolder}/bin/pip3.6 install -r {sourceFolder}/requirements.txt")


def updateDatabase(sourceFolder):
    run(f"cd {sourceFolder} && ../virtualenv/bin/python3.6 manage.py migrate --noinput")


def updateStatic(sourceFolder):
    run(f"cd {sourceFolder} && ../virtualenv/bin/python3.6 manage.py collectstatic")


def makeService():
    siteName = env.host
    siteFolder = f"/home/{env.user}/nginx/sites/{siteName}"
    sourceFolder = f"{siteFolder}/source"

    sitesAvailableCfg = f"/etc/nginx/sites-available/{siteName}"

    sudo(f"cp {sourceFolder}/deoloy-tools/nginx-site-avalabel.conf {sitesAvailableCfg}")
    sed(sitesAvailableCfg, "SITENAME", siteName, use_sudo=True)
    sed(sitesAvailableCfg, "PORT", "80", use_sudo=True)
    if not exists(f"/etc/nginx/sites-enabled/{siteName}"):
        sudo(f"ln -s /etc/nginx/sites-available/{siteName} /etc/nginx/sites-enabled/{siteName}")
    if exists(f"/etc/nginx/sites-enabled/default"):
        sudo("rm /etc/nginx/sites-enabled/default")

    servisePath = f"/etc/systemd/system/{siteName}.service"
    sudo(f"cp {sourceFolder}/deoloy-tools/gunicorn-SITENAME.service {servisePath}")
    sed(servisePath, "SITENAME", siteName, use_sudo=True)
    sudo("systemctl daemon-reload")
    sudo(f"systemctl enable {siteName}")
    sudo(f"systemctl start {siteName}")
    sudo(f"systemctl status {siteName}")

# if __name__ == "__main__":
#     sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
#     sys.exit(main())
