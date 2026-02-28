import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, resumo):
    texto = (vaga + " " + resumo).lower()
    if any(term in texto for term in ["superior", "graduação", "analista", "técnico"]):
        return "Especializado / Técnico"
    return "Operacional"

def minerar():
    # Setores estratégicos para a RMSP
    setores = ["Logística", "Varejo", "Indústria", "Saúde", "Serviços", "Construção"]
    banco = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    for setor in setores:
        print(f"Minerando setor: {setor}...")
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-sao-paulo"
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                cards = soup.find_all('li', class_='vaga')

                for card in cards:
                    try:
                        titulo = card.find('a', class_='link-detalhes-vaga').get_text(strip=True)
                        empresa = card.find('span', class_='vaga__empresa').get_text(strip=True)
                        local = card.find('span', class_='vaga__localizacao').get_text(strip=True)
                        resumo = card.find('div', class_='detalhes').get_text(strip=True)

                        banco.append({
                            "setor": setor,
                            "empresa": empresa,
                            "vaga": titulo,
                            "local": local,
                            "perfil": definir_perfil(titulo, resumo),
                            "qualificacao": resumo[:160]
                        })
                    except: continue
            else:
                print(f"Acesso negado ao setor {setor} (Status {res.status_code})")
        except Exception as e:
            print(f"Erro na conexão: {e}")

    # Salva o resultado para o Dashboard
    os.makedirs('data', exist_ok=True)
    output = {
        "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_vagas": len(banco),
        "vagas": banco
    }

    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Sucesso! {len(banco)} vagas capturadas.")

if __name__ == "__main__":
    minerar()
