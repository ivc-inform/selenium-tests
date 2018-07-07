from fabric.context_managers import settings
from fabric.operations import run
from fabric.state import env


def _get_manage_dot_py(host, user_name):
    return f"/home/{user_name}/sites/{host}/virtualenv/bin/python /home/{user_name}/sites/{host}/source/manage.py"


def reset_database(host, user_name):
    manage_dot_py = _get_manage_dot_py(host, user_name)
    with settings(host_string=f"{user_name}@{host}"):
        run(f"{manage_dot_py} flush --noinput")


def create_session_on_server(host, user_name, email):
    manage_dot_py = _get_manage_dot_py(host, user_name)
    with settings(host_string=f"{user_name}@{host}"):
        session_key = run(f"{manage_dot_py} create_session {email}")
        return session_key.strip()
