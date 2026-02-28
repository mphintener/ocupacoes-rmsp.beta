import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, qualificacao):
    texto = (vaga + " " + qualificacao).lower()
    if "superior" in texto or "graduação" in texto: return "Especializado"
    return "Operacional"

def minerar():
    setores = ["Logística", "Varejo", "Indústria", "Serviços"]
    banco = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for setor in setores:
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-grande-sao-paulo"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            cards = soup.find_all('li', class_='vaga')
            for card in cards:
                banco.append({
                    "setor": setor,
                    "empresa": card.find('span', class_='vaga__empresa').text.strip(),
                    "vaga": card.find('a', class_='link-detalhes-vaga').text.strip(),
                    "local": card.find('span', class_='vaga__localizacao').text.strip(),
                    "perfil": definir_perfil(card.find('a', class_='link-detalhes-vaga').text, card.find('div', class_='detalhes').text),
                    "qualificacao": card.find('div', class_='detalhes').text.strip()[:150]
                })
        except: continue

    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "total_vagas": len(banco),
            "vagas": banco
        }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    minerar()
