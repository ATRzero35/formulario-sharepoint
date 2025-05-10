from flask import Flask, request, jsonify
from shareplum import Site, Office365
from datetime import datetime
import os
import logging

app = Flask(__name__)

# Configura logging extensivo
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Log de entrada
        logger.debug(f"Dados recebidos: {request.json}")
        
        # Validação básica
        if not request.is_json:
            return jsonify({"error": "Envie JSON no header 'Content-Type: application/json'"}), 400
            
        data = request.get_json()
        
        # Conexão DEBUG - remova após testes
        logger.debug("Tentando conectar ao SharePoint...")
        try:
            auth = Office365(
                os.getenv("SHAREPOINT_URL"),
                username=os.getenv("SHAREPOINT_USER"),
                password=os.getenv("SHAREPOINT_PASS")
            ).GetCookies()
            site = Site(os.getenv("SHAREPOINT_SITE"), auth=auth)
            lista = site.List('FormularioApp')
            logger.debug("Conexão OK!")
        except Exception as e:
            logger.error(f"ERRO SharePoint: {str(e)}")
            return jsonify({"error": "Falha na conexão com SharePoint"}), 500

        # Processamento
        novo_id = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 3. Salvar no SharePoint
        lista.UpdateListItems(data=[{
            "Title": novo_id,
            "Nome": data.get('nome', 'Teste'),
            "Operacao": data.get('operacao', 'OPCAO1'),
            "DataEnvio": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "IDUnico": novo_id
        }], kind="New")

        return jsonify({"success": True, "id_unico": novo_id})

    except Exception as e:
        logger.exception("ERRO INTERNO:")
        return jsonify({"error": "Erro no servidor"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)