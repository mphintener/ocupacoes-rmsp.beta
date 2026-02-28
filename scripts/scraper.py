import json
import os
from datetime import datetime

def capturar_vagas():
    # Estrutura de dados focada em Qualificação e Perfil de Vaga (Toyotismo)
    vagas = [
        {
            "empresa": "Centro Logístico Anhanguera",
            "vaga": "Operador de Empilhadeira",
            "salario": 2350.00,
            "qualificacao": "Curso NR11, Ensino Médio",
            "local": "Caieiras - SP",
            "setor": "Logística"
        },
        {
            "empresa": "Varejo Express Franco",
            "vaga": "Assistente de Estoque",
            "salario": 1890.00,
            "qualificacao": "Informática Básica",
            "local": "Franco da Rocha - Centro",
            "setor": "Comércio"
        },
        {
            "empresa": "Tele-Serviços Lapa",
            "vaga": "Atendente de Suporte",
            "salario": 1550.00,
            "qualificacao": "Digitação, Boa Comunicação",
            "local": "São Paulo - Lapa",
            "setor": "Serviços"
        }
    ]

    os.makedirs('data', exist_ok=True)
    with open('data/inteligencia.json', 'w', encoding='utf-8') as f:
        json.dump({
            "projeto": "Ocupações RMSP",
            "atualizado": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "vagas": vagas
        }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    capturar_vagas()
