from fabric.api import env
from fabric.contrib.files import exists
from fabric.operations import run, local, sudo

REPO_URL = "https://github.com/ivc-inform/selenium-tests.git"


# fab -u uandrew -p dfqc2  --sudo-password='dfqc2' deploy:host=192.168.0.104

def deploy():
    site_folder = f"/home/{env.user}/nginx/sites/{env.host}"
    source_folder = f"{site_folder}/source"

    sudo("apt install apache2-utils")
    sudo("add-apt-repository --yes ppa:fkrull/deadsnakes")
    sudo("apt update")
    sudo("apt install nginx git python3.6 python3.6-venv git")

    createDirectoryStructure(site_folder)
    getSources(source_folder)


def createDirectoryStructure(site_folder):
    for subfolder in ("database", "source", "static", "virtualenv"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def getSources(source_folder):
    if exists(f"{source_folder}/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")

    current_commit = local("git log -n 1 --format=%H" , capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")
