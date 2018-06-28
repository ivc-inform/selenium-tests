import random

from fabric.api import env
from fabric.contrib.files import exists, sed, append
from fabric.operations import run, local, sudo

REPO_URL = "https://github.com/ivc-inform/selenium-tests.git"


# ab -u uandrew -p dfqc2 --sudo-password=dfqc2 -H 192.168.0.104 deploy

def deploy():
    siteName = env.host
    siteFolder = f"/home/{env.user}/nginx/sites/{siteName}"
    sourceFolder = f"{siteFolder}/source"

    # sudo("apt install apache2-utils")
    # sudo("add-apt-repository --yes ppa:fkrull/deadsnakes")
    # sudo("apt update")
    # sudo("apt install nginx git python3.6 python3.6-venv git")
    #
    # createDirectoryStructure(siteFolder)
    # getSources(sourceFolder)
    updateSetting(sourceFolder, siteName)


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
    sed(settingPath, "DEBUG=True", "DEBUG=False")
    sed(settingPath, "ALLOWED_HOSTS=.+$", f"ALLOWED_HOSTS=[{siteName}]")

    secretKeyFile = f"{sourceFolder}/project/secret_key.py"
    if not exists(secretKeyFile):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secretKeyFile, f"SECRET_KEY={key}")
    append(settingPath, "\nfrom .secret_key import SECRET_KEY")


if __name__ == "__main__":
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
    print(key)
