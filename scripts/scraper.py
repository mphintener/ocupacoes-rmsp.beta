import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time

def minerar_rmsp_exaustivo():
    # 1. MATRIZ TERRITORIAL: 39 Municípios da RMSP + 96 Distritos de SP
    municipios_rmsp = [
        "caieiras-sp", "cajamar-sp", "franco-da-rocha-sp", "francisco-morato-sp", "mairipora-sp",
        "guarulhos-sp", "osasco-sp", "barueri-sp", "itapevi-sp", "carapicuiba-sp", "santana-de-parnaiba-sp",
        "santo-andre-sp", "sao-bernardo-do-campo-sp", "sao-caetano-do-sul-sp", "diadema-sp", "maua-sp",
        "mogi-das-cruzes-sp", "suzano-sp", "itaquaquecetuba-sp", "taboao-da-serra-sp", "embu-das-artes-sp"
    ]
    
    # Amostra dos 96 distritos de SP (Sintaxe de URL: bairro-sao-paulo-sp)
    distritos_sp = [
        "lapa", "pinheiros", "se", "republica", "bras", "belem", "tatuape", "itaim-paulista", 
        "grajau", "capao-redondo", "brasilandia", "tremembe", "santana", "vila-mariana", 
        "santo-amaro", "itapegica", "ipiranga", "mooca", "perus", "anhanguera", "jaragua",
        "pirituba", "freguesia-do-o", "casa-verde", "cachoeirinha", "tucuruvi", "vila-guilherme"
        # O script abaixo concatena '-sao-paulo-sp' automaticamente para todos
    ]

    # 2. MATRIZ SETORIAL AMPLIADA
    setores = [
        "servicos-em-geral", "tecnologia-da-informacao", "comercio-varejista", 
        "saude", "educacao", "escritorios", "industrias", "transportadoras-e-logistica",
        "gastronomia", "construcao-civil"
    ]
    
    banco_total = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    # Unindo municípios e distritos na lista de busca
    locais_busca = municipios_rmsp + [f"{d}-sao-paulo-sp" for d in distritos_sp]

    print(f"🛰️ Iniciando Varredura em {len(locais_busca)} localidades x {len(setores)} setores...")

    for local in locais_busca:
        for setor in setores:
            url = f"https://www.guiamais.com.br/{local}/{setor}"
            print(f"🔍 Mapeando: {local.upper()} | {setor.upper()}")
            
            try:
                res = requests.get(url, headers=headers, timeout=10)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    itens = soup.find_all('div', class_='itemWrapper')

                    for item in itens:
                        try:
                            nome = item.find(['h2', 'a']).get_text(strip=True)
                            endereco = item.find('span', class_='address').get_text(strip=True) if item.find('span', class_='address') else "Local fixo"
                            
                            banco_total.append({
                                "setor": setor.replace("-", " ").title(),
                                "unidade": nome,
                                "local": endereco,
                                "territorio": local.replace("-sp", "").replace("-sao-paulo", "").replace("-", " ").title(),
                                "data_mapeamento": datetime.now().strftime('%d/%m/%Y')
                            })
                        except: continue
                
                # Delay curto para não ser bloqueado (Analista de Dados prevenido)
                time.sleep(0.3) 
            except Exception as e:
                print(f"⚠️ Erro em {local}: {e}")

    # 3. SALVAMENTO DA BASE DE DADOS
    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "total_unidades": len(banco_total),
            "vagas": banco_total # Compatível com index.html
        }, f, ensure_ascii=False, indent=4)
    
    print(f"🏁 MAPEAMENTO FINALIZADO: {len(banco_total)} pontos identificados.")

if __name__ == "__main__":
    minerar_rmsp_exaustivo()
