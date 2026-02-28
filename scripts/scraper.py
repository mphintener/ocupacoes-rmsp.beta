import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def definir_perfil(vaga, resumo):
    texto = (vaga + " " + resumo).lower()
    if any(t in texto for t in ["superior", "graduação", "analista", "técnico", "especialista"]):
        return "Especializado / Técnico"
    return "Operacional"

def minerar():
    # Setores diversificados para garantir volume na RMSP
    setores = ["Logistica", "Varejo", "Industria", "Saude", "Servicos", "Construção"]
    banco = []
    
    # User-Agent atualizado para simular Chrome real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.vagas.com.br/"
    }

    for setor in setores:
        print(f"Buscando setor: {setor}...")
        # URL simplificada para evitar filtros que quebram a busca
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-sao-paulo"
        
        try:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Buscamos por qualquer <li> que tenha 'vaga' no nome da classe
                vagas_encontradas = soup.select('li[class*="vaga"]')

                for item in vagas_encontradas:
                    try:
                        # Seletores mais flexíveis (pegando links e spans internos)
                        titulo = item.find('a', class_='link-detalhes-vaga').get_text(strip=True)
                        empresa = item.find('span', class_='vaga__empresa').get_text(strip=True)
                        local = item.find('span', class_='vaga__localizacao').get_text(strip=True)
                        resumo = item.find('div', class_='detalhes').get_text(strip=True)

                        banco.append({
                            "setor": setor,
                            "empresa": empresa,
                            "vaga": titulo,
                            "local": local,
                            "perfil": definir_perfil(titulo, resumo),
                            "qualificacao": resumo[:180],
                            "data_coleta": datetime.now().strftime('%d/%m/%Y')
                        })
                    except:
                        continue
            else:
                print(f"Acesso negado ({res.status_code}) ao setor {setor}")
        except Exception as e:
            print(f"Erro de conexão: {e}")

    # Consolidação dos dados
    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "total_vagas": len(banco),
            "vagas": banco
        }, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Finalizado! {len(banco)} vagas capturadas para a RMSP.")

if __name__ == "__main__":
    minerar()
