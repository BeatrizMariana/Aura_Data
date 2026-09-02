import pandas as pd
import numpy as np
from datetime import datetime

def executar_etl():
    print("Iniciando o processo de ETL e Validacao dos Dados...")

    # 1. Extracao (Simulando uma massa de dados bruta com inconsistencias propositais)
    dados_brutos = {
        'timestamp': ['2026-09-01 08:00:00', '2026-09-01 09:00:00', '2026-09-01 10:00:00', '2026-09-01 10:00:00', '2026-09-01 11:00:00'],
        'estacao': ['Centro', 'Centro', 'Pinheiros', 'Pinheiros', 'Zona Sul'],
        'pm25': [22.4, -5.0, 35.2, 35.2, None], 
        'pm10': [45.1, 50.2, 60.0, 60.0, 75.5],
        'temperatura': [25.5, 26.0, 27.2, 27.2, 28.1],
        'status_qualidade': ['Boa', 'Moderada', 'Ruim', 'Ruim', 'Moderada']
    }

    df = pd.DataFrame(dados_brutos)
    print(f"Dados brutos carregados: {len(df)} registros.")

    # 2. Transformacao e Aplicacao dos Pilares de Governanca
    df['pm25'] = df['pm25'].apply(lambda x: np.nan if x is not None and x < 0 else x)
    df['pm25'] = df['pm25'].fillna(df['pm25'].mean())
    df = df.drop_duplicates()
    print(f"Registros apos remocao de duplicatas (Unicidade): {len(df)}")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['data'] = df['timestamp'].dt.date
    df['hora'] = df['timestamp'].dt.time
    df['aqi_medio'] = (df['pm25'] * 1.5 + df['pm10'] * 0.8) / 2

    # 3. Carga (Salvando o arquivo ajustado)
    nome_arquivo = "cidade_alfa_qualidade_ar_ajustado.xlsx"
    df.to_excel(nome_arquivo, index=False)
    print(f"ETL Concluido com sucesso! Arquivo salvo como: {nome_arquivo}")

if __name__ == "__main__":
    executar_etl()
