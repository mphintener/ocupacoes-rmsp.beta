import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, qualificacao):
    texto = (vaga + " " + qualificacao).lower()
    if "superior" in texto or "graduação" in texto or "analista" in texto:
        return "Especializado / Técnico"
    return "Operacional"

def minerar():
    # Setores diversificados para garantir que o balde não venha vazio
    setores = ["Logística", "Varejo", "Indústria", "Serviços", "Saúde", "Construção"]
    banco = []
    
    # Cabeçalho de navegador real (essencial para não ser bloqueado)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    for setor in setores:
        # URL de busca direta na Grande São Paulo
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-sao-paulo"
        
        try:
            print(f"Buscando setor: {setor}...")
            res = requests.get(url, headers=headers, timeout=15)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # A tag correta das vagas no portal atualizado
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
                    except:
                        continue
            else:
                print(f"Erro no acesso ({res.status_code}) ao setor {setor}")
        except Exception as e:
            print(f"Falha na conexão: {e}")

    # Consolidação final
    os.makedirs('data', exist_ok=True)
    dados_finais = {
        "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_vagas": len(banco),
        "vagas": banco
    }

    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False, indent=4)
    
    print(f"Finalizado! {len(banco)} vagas capturadas.")

if __name__ == "__main__":
    minerar()
