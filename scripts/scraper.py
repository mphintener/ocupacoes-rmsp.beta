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
    # Lista focada nos motores de emprego da Grande SP
    setores = ["Logística", "Varejo", "Indústria", "Serviços", "Saúde", "Administrativo"]
    banco = []
    
    # Cabeçalho robusto para evitar bloqueio (User-Agent real)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    for setor in setores:
        print(f"Buscando {setor} na RMSP...")
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-sao-paulo"
        
        try:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code != 200:
                print(f"Erro no acesso ao setor {setor}: Status {res.status_code}")
                continue
            
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
                        "qualificacao": resumo[:180]
                    })
                except: continue
        except Exception as e:
            print(f"Falha na conexão: {e}")

    # Salva o arquivo final
    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "total_vagas": len(banco),
            "vagas": banco
        }, f, ensure_ascii=False, indent=4)
    
    print(f"Processo concluído. Encontradas {len(banco)} vagas.")

if __name__ == "__main__":
    minerar()
