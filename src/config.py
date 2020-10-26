import os
from dotenv import load_dotenv

load_dotenv()

YA_TOKEN = os.environ.get('YA_TOKEN', None)
MOESIF_TOKEN = os.environ.get('MOESIF_TOKEN', None)
