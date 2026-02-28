import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, qualificacao):
    texto = (vaga + " " + qualificacao).lower()
    if "superior" in texto or "graduação" in texto: return "Especializado"
    return "Operacional"

def minerar_rmsp():
    # Lista ampla de setores para capturar a RMSP
    setores = ["Logística", "Varejo", "Indústria", "Serviços", "Saúde", "Construção"]
    banco = []
    
    # Cabeçalho para evitar bloqueio do portal
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for setor in setores:
        print(f"Rastreando {setor}...")
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-grande-sao-paulo"
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                cards = soup.find_all('li', class_='vaga')

                for card in cards:
                    try:
                        titulo = card.find('a', class_='link-detalhes-vaga').text.strip()
                        empresa = card.find('span', class_='vaga__empresa').text.strip()
                        local = card.find('span', class_='vaga__localizacao').text.strip()
                        resumo = card.find('div', class_='detalhes').text.strip()

                        banco.append({
                            "setor": setor,
                            "empresa": empresa,
                            "vaga": titulo,
                            "local": local,
                            "perfil": definir_perfil(titulo, resumo),
                            "qualificacao": resumo[:180]
                        })
                    except: continue
        except Exception as e:
            print(f"Erro em {setor}: {e}")

    # Consolidação dos dados para o Dashboard
    os.makedirs('data', exist_ok=True)
    output = {
        "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_vagas": len(banco),
        "vagas": banco
    }

    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"Finalizado: {len(banco)} vagas capturadas.")

if __name__ == "__main__":
    minerar_rmsp()
