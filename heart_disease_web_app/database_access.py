from pymongo import MongoClient
from settings import DATABASES

client = MongoClient(DATABASES['default']['CLIENT']['host'])
db = client['heart_disease_web_app']
