import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# 1. DEFINIÇÃO DA LÓGICA DE PERFIL (Colocamos no topo para o script conhecer a função)
def definir_perfil(vaga, qualificacao):
    """
    Lógica de analista: cruza palavras-chave para definir o nível técnico/operacional
    """
    texto_analise = (vaga + " " + qualificacao).lower()
    
    if "superior" in texto_analise or "especialização" in texto_analise or "graduação" in texto_analise:
        return "Especializado / Técnico"
    elif "experiência" in texto_analise or "médio" in texto_analise or "técnico" in texto_analise:
        return "Operacional Qualificado"
    else:
        return "Operacional de Entrada"

def minerar_mercado_rmsp():
    # LISTA AMPLIADA: Setores estratégicos da RMSP para mapeamento total
    setores = [
        "Logística", "Transportes", "Depósito", "Indústria", "Manutenção", 
        "Varejo", "Supermercado", "Comércio", "Serviços", "Administrativo", 
        "Telemarketing", "Atendimento", "Saúde", "Hospitalar", "Construção Civil", 
        "Segurança", "Limpeza", "Gastronomia", "Educação", "Tecnologia"
    ]
    banco_consolidado = []
    for setor in setores:
        url = f"https://www.vagas.com.br/vagas-de-{setor}-em-grande-sao-paulo"
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('li', class_='vaga')

            for card in cards:
                # Captura dos dados brutos
                titulo = card.find('a', class_='link-detalhes-vaga').text.strip()
                empresa = card.find('span', class_='vaga__empresa').text.strip()
                local = card.find('span', class_='vaga__localizacao').text.strip()
                resumo = card.find('div', class_='detalhes').text.strip()
                
                # --- O PULO DO GATO: CHAMADA DA FUNÇÃO DE PERFIL ---
                # Aqui o robô usa a função que definimos lá no topo
                perfil_vaga = definir_perfil(titulo, resumo)

                banco_consolidado.append({
                    "setor": setor,
                    "empresa": empresa,
                    "vaga": titulo,
                    "local": local,
                    "perfil": perfil_vaga, # <--- Nova Coluna de Dados
                    "qualificacao": resumo[:200],
                    "data_coleta": datetime.now().strftime('%d/%m/%Y')
                })
        except Exception as e:
            print(f"Erro no setor {setor}: {e}")

    # Consolidação e salvamento
    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "projeto": "Ocupações RMSP - Estatística Real",
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "total_vagas": len(banco_consolidado),
            "vagas": banco_consolidado
        }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    minerar_mercado_rmsp()
