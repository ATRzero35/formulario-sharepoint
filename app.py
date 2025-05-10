from flask import Flask, request, jsonify
from shareplum import Site, Office365
from datetime import datetime
import os

app = Flask(__name__)

# Configurações do SharePoint (substitua com seus dados)
SHAREPOINT_URL = "https://cevalogisticsoffice365-my.sharepoint.com"  # URL base do SharePoint
SHAREPOINT_SITE = "/personal/ext_hercules_souza_cruz_cevalogistics_com/Lists/"             # Caminho do site
SHAREPOINT_LIST = "FormularioApp"                 # Nome da lista
USERNAME = os.getenv("SHAREPOINT_USER")           # E-mail corporativo
PASSWORD = os.getenv("SHAREPOINT_PASS")           # Senha

def conectar_sharepoint():
    auth = Office365(SHAREPOINT_URL, username=USERNAME, password=PASSWORD).GetCookies()
    return Site(SHAREPOINT_SITE, auth=auth)

@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Dados do formulário
        dados = request.json
        nome = dados.get("nome")
        operacao = dados.get("operacao")  # "OPCAO1" ou "OPCAO2"
        
        # Conexão com SharePoint
        site = conectar_sharepoint()
        lista = site.List(SHAREPOINT_LIST)
        
        # 1. Buscar último contador
        itens = lista.GetListItems()
        ultimo_contador = max([int(item["Contador"]) for item in itens if item.get("Contador")]) if itens else 0
        
        # 2. Gerar ID único (OPCAOX-XXXX)
        novo_contador = ultimo_contador + 1
        id_unico = f"{operacao}-{novo_contador:04d}"  # Formato: OPCAO1-0001
        
        # 3. Salvar no SharePoint
        lista.UpdateListItems(data=[{
            "Title": id_unico,  # Campo obrigatório
            "Nome": nome,
            "Operacao": operacao,
            "DataEnvio": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "IDUnico": id_unico,
            "Contador": novo_contador
        }], kind="New")
        
        return jsonify({"success": True, "id_unico": id_unico})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)