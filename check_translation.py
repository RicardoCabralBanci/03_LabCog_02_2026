import os
import sys
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient
from azure.storage.blob import BlobServiceClient

load_dotenv("25. Scripts/.env")

TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
TARGET_CONTAINER = "output-docs"

def main():
    job_id = "2aae2e70-a7e3-40b1-8fb1-aba3fd5953df"
    client = DocumentTranslationClient(TRANSLATOR_ENDPOINT, AzureKeyCredential(TRANSLATOR_KEY))
    
    status = client.get_translation_status(job_id)
    print(f"Status Atual: {status.status}")
    
    if status.status == "Succeeded":
        print("Tradução concluída! Baixando...")
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(TARGET_CONTAINER)
        
        filename = "BA 89503126_000100 _Innopal_EN.pdf"
        blob_client = container_client.get_blob_client(filename)
        
        dest_path = os.path.join("25. Scripts/WORD_PDF", "BA 89503126_000100 _Innopal_PT.pdf")
        with open(dest_path, "wb") as f:
            f.write(blob_client.download_blob().readall())
        print(f"Sucesso! Arquivo salvo como: {dest_path}")
    elif status.status == "Failed":
        for doc in client.list_document_statuses(job_id):
            if doc.status == "Failed":
                print(f"Erro no documento: {doc.error.code} - {doc.error.message}")
    else:
        print("O Azure ainda está trabalhando no arquivo. Tente novamente em 1 ou 2 minutos.")

if __name__ == "__main__":
    main()