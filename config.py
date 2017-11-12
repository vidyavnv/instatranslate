from azure.storage.blob import BlockBlobService
from pymongo import MongoClient

from constants import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, CONTAINER, MONGO_URI


block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME, account_key=AZURE_ACCOUNT_KEY)
block_blob_service.create_container(CONTAINER)


mongo_client = MongoClient(MONGO_URI)
db = mongo_client['instatranslatordb']
VIDEOS_COLLECTION = db['videos']
REQUEST_COLLECTION = db['requests']