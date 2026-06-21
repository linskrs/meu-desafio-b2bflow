import os
import logging
import requests
from dotenv import load_dotenv

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

def buscar_contatos() -> list:
    """Busca até 3 contatos cadastrados no Supabase via requisição HTTP direta."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        logging.error("Variáveis de ambiente do Supabase não configuradas no .env.")
        return []
    
    # Remove barras duplicadas da URL se houver
    url_base = SUPABASE_URL.strip().rstrip('/')
    url = f"{url_base}/rest/v1/contatos?select=nome,telefone&limit=3"
    
    headers = {
        "apikey": SUPABASE_KEY.strip(),
        "Authorization": f"Bearer {SUPABASE_KEY.strip()}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Erro na API do Supabase: Status {response.status_code} - {response.text}")
            return []
    except Exception as e:
        logging.error(f"Erro ao conectar ao Supabase via HTTP: {e}")
        return []

def enviar_mensagem_zapi(nome: str, telefone: str):
    """Envia a mensagem exata exigida pelo desafio via Z-API ou simula caso chaves estejam vazias."""
    if not ZAPI_INSTANCE_ID or not ZAPI_TOKEN:
        logging.info(f"[SIMULAÇÃO Z-API] Enviando para {nome} ({telefone}): Olá, {nome} tudo bem com você?")
        return

    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN if ZAPI_CLIENT_TOKEN else ""
    }
    
    payload = {
        "phone": telefone,
        "message": f"Olá, {nome} tudo bem com você?"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            logging.info(f"Mensagem enviada com sucesso para {nome} ({telefone}).")
        else:
            logging.warning(f"Falha ao enviar para {nome}. Status: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de rede na Z-API: {e}")

def main():
    logging.info("Iniciando o fluxo de disparo de mensagens...")
    contatos = buscar_contatos()
    
    if not contatos:
        logging.warning("Nenhum contato encontrado ou falha na integração com o banco.")
        return

    logging.info(f"Sucesso: {len(contatos)} contato(s) carregado(s). Iniciando envios...")
    for contato in contatos:
        nome = contato.get("nome")
        telefone = contato.get("telefone")
        
        if nome and telefone:
            enviar_mensagem_zapi(nome, telefone)

if __name__ == "__main__":
    main()