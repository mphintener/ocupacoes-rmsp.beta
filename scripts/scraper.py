import json
import os
from datetime import datetime

def processar_vagas_rmsp(lista_vagas_coletadas):
    """
    O Pulo do Gato: Estrutura qualquer vaga da RMSP capturada 
    focando no perfil de exploração e qualificação técnica.
    """
    os.makedirs('data', exist_ok=True)
    
    # Adiciona metadados da pesquisa de doutorado
    banco_de_dados = {
        "projeto": "Ocupações RMSP - Inteligência do Trabalhador",
        "pesquisa": "Monitoramento de Qualificação e Rendimento Real",
        "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_vagas_mapeadas": len(lista_vagas_coletadas),
        "vagas": lista_vagas_coletadas
    }

    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump(banco_de_dados, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # EXEMPLO DE ENTRADA DINÂMICA (AQUI O ROBÔ RECEBE O QUE ENCONTRAR NA RMSP)
    # No futuro, essa lista será preenchida por um Crawler automático.
    vagas_do_dia = [
        {
            "empresa": "Amazon Logística", 
            "vaga": "Auxiliar de Operações", 
            "salario": 1850.00, 
            "qualificacao": "Ensino Médio, Disponibilidade Total", 
            "local": "Cajamar - SP", # Fora do eixo inicial
            "setor": "Logística (Toyotismo)"
        },
        {
            "empresa": "Itaú Unibanco", 
            "vaga": "Operador de Atendimento", 
            "salario": 2100.00, 
            "qualificacao": "Superior cursando, CPA-10", 
            "local": "São Paulo - Centro", 
            "setor": "Financeiro"
        },
        {
            "empresa": "Pão de Açúcar", 
            "vaga": "Repositor Especializado", 
            "salario": 1650.00, 
            "qualificacao": "Experiência em Perecíveis", 
            "local": "Santo André - ABC", # Expandindo para o ABC
            "setor": "Varejo"
        },
        {
            "empresa": "Hosp. Albert Einstein", 
            "vaga": "Auxiliar Administrativo", 
            "salario": 2400.00, 
            "qualificacao": "Curso de Gestão Hospitalar", 
            "local": "São Paulo - Morumbi", 
            "setor": "Saúde"
        }
    ]
    
    processar_vagas_rmsp(vagas_do_dia)
