import pandas as pd
import numpy as np

def executar_etl():
    print("Iniciando o processo de ETL com a estrutura completa de colunas...")

    # 1. Extracao com todas as colunas solicitadas
    dados_brutos = {
        'id_coleta': ['COL001', 'COL002', 'COL003', 'COL004', 'COL005'],
        'id_ponto_monitoramento': ['PNT01', 'PNT02', 'PNT03', 'PNT04', 'PNT05'],
        'data_coleta': ['2026-09-01 08:00:00', '2026-09-01 09:00:00', '2026-09-01 10:00:00', '2026-09-01 10:00:00', '2026-09-01 11:00:00'],
        'regiao': ['Centro', 'Sul', 'Oeste', 'Oeste', 'Norte'],
        'bairro': ['Liberdade', 'Morumbi', 'Pinheiros', 'Pinheiros', 'Santana'],
        'tipo_area': ['Urbana', 'Residencial', 'Comercial', 'Comercial', 'Mista'],
        'temperatura_c': [22.5, 24.0, 26.1, 26.1, 27.8],
        'umidade_%': [65, 58, 52, 52, 48],
        'velocidade_vento_kmh': [12.0, 8.5, 15.2, 15.2, 6.0],
        'chuva_mm': [0.0, 0.0, 1.2, 1.2, 0.0],
        'pm25_ug_m3': [18.5, 25.0, 12.1, 12.1, 38.4],
        'pm10_ug_m3': [42.0, 55.3, 30.0, 30.0, 72.1],
        'co_ppm': [0.8, 1.2, 0.5, 0.5, 1.7],
        'no2_ppb': [25.4, 32.1, 18.0, 18.0, 45.0],
        'o3_ppb': [40.2, 48.6, 35.1, 35.1, 60.2],
        'indice_qualidade_ar': [45, 62, 30, 30, 85],
        'qualidade_percebida': ['Boa', 'Moderada', 'Boa', 'Boa', 'Ruim']
    }

    df = pd.DataFrame(dados_brutos)

    # 2. Transformacao e Governanca (Unicidade e Tratamento)
    df = df.drop_duplicates()
    df['data_coleta'] = pd.to_datetime(df['data_coleta'])

    # 3. Carga
    nome_arquivo = "cidade_alfa_qualidade_ar_ajustado.xlsx"
    df.to_excel(nome_arquivo, index=False)
    print(f"ETL concluido! Planilha gerada com todas as colunas em: {nome_arquivo}")

if __name__ == "__main__":
    executar_etl()
