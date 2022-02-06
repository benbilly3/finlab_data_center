import os
import datetime
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))


def git_init(work_dir):
    user_name = os.getenv("GITLAB_NAME", settings.CONFIG_DATA.get("GITLAB_NAME"))
    mail = os.getenv("GMAIL", settings.CONFIG_DATA.get("GMAIL"))
    os.chdir(work_dir)
    os.system(f"git config --global user.email {mail}")
    os.system(f"git config --global user.name {user_name}")
    os.system("git pull origin master")


def git_commit(add_dir='.'):
    now = datetime.datetime.now()
    now = str(now.strftime("%Y-%m-%d %H:%M"))
    os.system(f"git add {add_dir}")
    os.system("git commit -m '%s update data'" % now)
    os.system("git push -u origin master")
    info = "Finish!git push successfully"
    return info
