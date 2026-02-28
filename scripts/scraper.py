import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, qualificacao):
    texto = (vaga + " " + qualificacao).lower()
    if "superior" in texto or "graduação" in texto: return "Especializado"
    elif "experiência" in texto or "médio" in texto: return "Operacional Qualificado"
    return "Operacional de Entrada"

def minerar_rmsp():
    # Lista compacta para teste rápido
    setores = ["Logística", "Varejo", "Indústria", "Serviços"]
    banco = []
    
    # Cabeçalho que simula um navegador real para evitar bloqueio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    for setor in setores:
        print(f"Tentando minerar {setor}...")
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-grande-sao-paulo"
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200: continue
            
            soup = BeautifulSoup(res.text, 'html.parser')
            # Busca pela classe correta das vagas
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
            print(f"Erro no setor {setor}: {e}")

    # Garante que o diretório existe
    os.makedirs('data', exist_ok=True)
    
    output = {
        "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_vagas": len(banco),
        "vagas": banco
    }

    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"Sucesso! {len(banco)} vagas encontradas.")

if __name__ == "__main__":
    minerar_rmsp()
