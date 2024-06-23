from pathlib import Path
from django.urls import reverse

import os # para usar a dotenv
from utils.enviroment import get_env_variable, parse_comma_sep_str_to_list



if os.environ.get('DEBUG', None) is None: #SE NAO EXISTIR A CHAVE DEBUG NO .env ELE VAI CARREGAR O AMBIENTE VIRTUALQUANDO O DJANGO ACESSAR O settings.py(usei para resolver um problema do pytest nao carregar o ambiente virtual)
    from dotenv import load_dotenv
    load_dotenv()
    
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'Insecure')

DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS : list[str] = parse_comma_sep_str_to_list(get_env_variable('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS: list[str] = parse_comma_sep_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS'))


ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

