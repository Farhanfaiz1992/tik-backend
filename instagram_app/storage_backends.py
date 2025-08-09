# your_app/custom_storages.py
import os
from storages.backends.azure_storage import AzureStorage
from dotenv import load_dotenv
load_dotenv()


class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_STATIC_CONTAINER', 'static')
    expiration_secs = None


class AzureMediaStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_MEDIA_CONTAINER', 'media')
    expiration_secs = None
