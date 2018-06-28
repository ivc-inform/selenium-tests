from fabric.api import env
from fabric.operations import run

REPO_URL = "https://github.com/ivc-inform/selenium-tests.git"

# fab -u uandrew -p dfqc2  deploy:host=192.168.0.104

def deploy():
    site_folder = f"/home/{env.user}/nginx/sites/{env.host}"
    source_folder = f"{site_folder}/source"

    createDirectoryStructure(site_folder)


def createDirectoryStructure(site_folder):
    for subfolder in ("database", "source", "static", "virtualenv"):
        run(f"mkdir -p {site_folder}/{subfolder}")
