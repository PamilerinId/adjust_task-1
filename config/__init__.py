from os import path, environ
from dotenv import load_dotenv

env_path = path.join(path.dirname(__file__),'.env')
load_dotenv(env_path, override=True)


def get_env(key):
   return environ.get(key)
