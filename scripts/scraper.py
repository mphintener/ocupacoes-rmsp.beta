import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, qualificacao):
    texto = (vaga + " " + qualificacao).lower()
    if "superior" in texto or "graduação" in texto: return "Especializado / Técnico"
    elif "experiência" in texto or "médio" in texto: return "Operacional Qualificado"
    else: return "Operacional de Entrada"

def minerar_rmsp():
    # LISTA AMPLIADA PARA SAIR DE CAIEIRAS/FRANCO
    setores = ["Logística", "Indústria", "Varejo", "Serviços", "Saúde", "Construção"]
    banco = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for setor in setores:
        # A URL agora busca em toda a Grande São Paulo
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-grande-sao-paulo"
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            cards = soup.find_all('li', class_='vaga')

            for card in cards:
                titulo = card.find('a', class_='link-detalhes-vaga').text.strip()
                empresa = card.find('span', class_='vaga__empresa').text.strip()
                local = card.find('span', class_='vaga__localizacao').text.strip()
                resumo = card.find('div', class_='detalhes').text.strip()

                banco.append({
                    "setor": setor,
                    "empresa": empresa,
                    "vaga": titulo,
                    "local": local, # Aqui virá Lapa, Itaquera, Guarulhos, etc.
                    "perfil": definir_perfil(titulo, resumo),
                    "qualificacao": resumo[:180]
                })
        except: continue

    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "vagas": banco
        }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    minerar_rmsp()
