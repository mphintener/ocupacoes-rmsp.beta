import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def minerar_vagas_grande_sp(termo="Logística"):
    # URL focada na região metropolitana (Exemplo de busca em SP e arredores)
    url = f"https://www.vagas.com.br/vagas-de-{termo}-em-sao-paulo"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        vagas_capturadas = []

        # O robô varre os "cards" de vagas da página
        cards = soup.find_all('li', class_='vaga')

        for card in cards:
            # EXTRAÇÃO DINÂMICA
            titulo = card.find('a', class_='link-detalhes-vaga').text.strip()
            empresa = card.find('span', class_='vaga__empresa').text.strip()
            
            # O PULO DO GATO: Captura o Local (Município ou Distrito de SP)
            # Geralmente o site exibe: "São Paulo - Lapa" ou "Guarulhos"
            localizacao_bruta = card.find('span', class_='vaga__localizacao').text.strip()
            
            # Tratamento da Qualificação (Resumo da vaga)
            resumo = card.find('div', class_='detalhes').text.strip()[:150]

            vagas_capturadas.append({
                "empresa": empresa,
                "vaga": titulo,
                "local": localizacao_bruta, # Aqui virá o Distrito ou Município real
                "qualificacao": resumo,
                "salario": "A combinar",
                "setor": termo,
                "data_coleta": datetime.now().strftime('%d/%m')
            })

        # Salva o Banco de Dados para o seu PWA
        os.makedirs('data', exist_ok=True)
        with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
            json.dump({
                "projeto": "Monitoramento Ocupações RMSP",
                "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
                "vagas": vagas_capturadas
            }, f, ensure_ascii=False, indent=4)
            
        print(f"Sucesso: {len(vagas_capturadas)} vagas mapeadas na RMSP.")

    except Exception as e:
        print(f"Erro na mineração: {e}")

if __name__ == "__main__":
    minerar_vagas_grande_sp("Logística")
