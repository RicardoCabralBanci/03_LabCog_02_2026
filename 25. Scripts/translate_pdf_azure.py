import os
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Bibliotecas Azure
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

SOURCE_CONTAINER = "input-docs"
TARGET_CONTAINER = "output-docs"

def check_config():
    if not all([TRANSLATOR_KEY, TRANSLATOR_ENDPOINT, CONNECTION_STRING]):
        print("ERRO: Variáveis de ambiente não configuradas.")
        print("Por favor, preencha o arquivo .env com suas chaves do Azure.")
        sys.exit(1)

def get_blob_service_client():
    return BlobServiceClient.from_connection_string(CONNECTION_STRING)

def generate_sas_url(blob_service_client, container_name, permissions):
    """Gera uma URL SAS (Assinatura de Acesso Compartilhado) para o container."""
    sas_token = generate_container_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        account_key=blob_service_client.credential.account_key,
        permission=permissions,
        expiry=datetime.utcnow() + timedelta(hours=1) # Token válido por 1 hora
    )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}?{sas_token}"

def upload_file(blob_service_client, container_name, file_path):
    """Sobe o arquivo local para o container."""
    filename = os.path.basename(file_path)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    
    print(f"--> Uploading: {filename}...")
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return filename

def download_file(blob_service_client, container_name, filename, destination_folder):
    """Baixa o arquivo traduzido."""
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    
    # Prefixo para indicar tradução
    new_filename = f"TRADUZIDO_{filename}"
    dest_path = os.path.join(destination_folder, new_filename)
    
    print(f"--> Downloading: {new_filename}...")
    with open(dest_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    
    print(f"Sucesso! Arquivo salvo em: {dest_path}")
    return dest_path

def main():
    check_config()
    
    if len(sys.argv) < 3:
        print("Uso: python translate_pdf_azure.py <caminho_do_pdf> <idioma_destino>")
        print("Exemplo: python translate_pdf_azure.py meu_documento.pdf pt")
        sys.exit(1)

    file_path = sys.argv[1]
    target_language = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        sys.exit(1)

    print(f"--- Iniciando Tradução de Documentos (Azure) ---")
    print(f"Arquivo: {file_path}")
    print(f"Destino: {target_language}")

    # 1. Preparar Storage
    blob_service_client = get_blob_service_client()
    
    # Criar containers se não existirem
    try:
        blob_service_client.create_container(SOURCE_CONTAINER)
    except: pass # Já existe
    try:
        blob_service_client.create_container(TARGET_CONTAINER)
    except: pass # Já existe

    # 2. Upload do arquivo
    filename = upload_file(blob_service_client, SOURCE_CONTAINER, file_path)

    # 3. Gerar SAS Tokens (Permissões temporárias para o Tradutor ler/escrever)
    source_sas_url = generate_sas_url(blob_service_client, SOURCE_CONTAINER, ContainerSasPermissions(read=True, list=True))
    target_sas_url = generate_sas_url(blob_service_client, TARGET_CONTAINER, ContainerSasPermissions(write=True, list=True, read=True))

    # 4. Iniciar Tradução
    client = DocumentTranslationClient(TRANSLATOR_ENDPOINT, AzureKeyCredential(TRANSLATOR_KEY))

    print("--> Enviando job para o Azure AI Translator...")
    poller = client.begin_translation(
        source_url=source_sas_url,
        target_url=target_sas_url,
        target_language=target_language
    )

    print(f"Job ID: {poller.id}")
    print("Aguardando processamento (isso pode levar alguns minutos)...")
    
    result = poller.result()

    print(f"Status: {poller.status()}")
    
    found_doc = False
    for document in result:
        print(f"Documento: {document.source_document_url}")
        print(f"Status Doc: {document.status}")
        if document.status == "Succeeded":
            found_doc = True
        else:
            print(f"Erro: {document.error.code} - {document.error.message}")

    # 5. Download do Resultado
    if found_doc:
        # Nota: O Azure pode manter o mesmo nome ou alterar dependendo da configuração, 
        # mas por padrão mantém o nome do arquivo no container de destino.
        output_dir = os.path.dirname(file_path)
        download_file(blob_service_client, TARGET_CONTAINER, filename, output_dir)
        
        # Limpeza opcional (comentada por segurança)
        # blob_service_client.get_blob_client(SOURCE_CONTAINER, filename).delete_blob()
        # blob_service_client.get_blob_client(TARGET_CONTAINER, filename).delete_blob()
    else:
        print("A tradução falhou ou não retornou documentos válidos.")

if __name__ == "__main__":
    main()
