import os
from django.core.management.base import BaseCommand
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    help = 'Create required Azure Blob Storage containers'

    def handle(self, *args, **kwargs):
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not conn_str:
            self.stderr.write("ERROR: AZURE_STORAGE_CONNECTION_STRING not found in environment.")
            return

        containers = ['static', 'media']  # Add any containers you want
        service_client = BlobServiceClient.from_connection_string(conn_str)

        for container_name in containers:
            try:
                container_client = service_client.get_container_client(container_name)
                container_client.create_container()
                self.stdout.write(self.style.SUCCESS(f"Created container: {container_name}"))
            except Exception as e:
                self.stdout.write(f"Skipping container '{container_name}' (may already exist): {e}")
