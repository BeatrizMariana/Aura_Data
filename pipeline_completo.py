import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def gerar_dataset_base():
    estacoes = [
        {"id": f"PNT{i:02d}", "regiao": reg, "bairro": bairro, "tipo": tipo}
        for i, (reg, bairro, tipo) in enumerate([
            ("Centro", "Liberdade", "Urbana"),
            ("Sul", "Morumbi", "Residencial"),
            ("Oeste", "Pinheiros", "Comercial"),
            ("Norte", "Santana", "Mista"),
            ("Leste", "Itaquera", "Urbana"),
            ("Sudeste", "Ipiranga", "Comercial"),
            ("Noroeste", "Pirituba", "Residencial"),
            ("Sudoeste", "Butantã", "Urbana"),
            ("Nordeste", "Tucuruvi", "Mista"),
            ("Centro-Sul", "Vila Mariana", "Residencial")
        ], start=1)
    ]
    registros = []
    contador = 1
    data_inicial = datetime.now() - timedelta(days=21)
    np.random.seed(42)
    
    for est in estacoes:
        for passo in range(500):
            data_atual = data_inicial + timedelta(hours=passo)
            temp = round(float(np.random.normal(24.0, 4.0)), 1)
            umid = int(np.clip(np.random.normal(60, 15), 20, 95))
            vento = round(float(np.clip(np.random.exponential(5.0) + 2, 1, 30)), 1)
            chuva = round(float(np.random.choice([0.0, 0.5, 2.1, 5.4], p=[0.85, 0.08, 0.05, 0.02])), 1)
            pm25 = round(float(np.clip(np.random.normal(22.0, 10.0), 2, 120)), 1)
            pm10 = round(float(pm25 * np.random.uniform(1.8, 2.5)), 1)
            co = round(float(np.clip(np.random.normal(0.8, 0.3), 0.1, 5.0)), 2)
            no2 = round(float(np.clip(np.random.normal(25.0, 8.0), 5, 90)), 1)
            o3 = round(float(np.clip(np.random.normal(35.0, 12.0), 5, 140)), 1)
            aqi = int(pm25 * 1.3 + no2 * 0.2)
            aqi = max(10, min(300, aqi))
            qualidade = "Boa" if aqi <= 50 else ("Moderada" if aqi <= 100 else ("Ruim" if aqi <= 199 else "Muito Ruim"))
            
            registros.append({
                'id_coleta': f"COL{contador:05d}",
                'id_ponto_monitoramento': est['id'],
                'data_coleta': data_atual.strftime('%Y-%m-%d %H:%M:%S'),
                'regiao': est['regiao'],
                'bairro': est['bairro'],
                'tipo_area': est['tipo'],
                'temperatura_c': temp,
                'umidade_%': umid,
                'velocidade_vento_kmh': vento,
                'chuva_mm': chuva,
                'pm25_ug_m3': pm25,
                'pm10_ug_m3': pm10,
                'co_ppm': co,
                'no2_ppb': no2,
                'o3_ppb': o3,
                'indice_qualidade_ar': aqi,
                'qualidade_percebida': qualidade
            })
            contador += 1
    return pd.DataFrame(registros)

if __name__ == "__main__":
    print("Gerando bases original e ajustada com dicionario de dados...")
    
    # 1. Gera o DataFrame Original
    df_original = gerar_dataset_base()
    
    # Dicionário de Dados padrão
    df_dicionario = pd.DataFrame({
        "Coluna": ["id_coleta", "id_ponto_monitoramento", "data_coleta", "regiao", "bairro", "tipo_area", "temperatura_c", "umidade_%", "velocidade_vento_kmh", "chuva_mm", "pm25_ug_m3", "pm10_ug_m3", "co_ppm", "no2_ppb", "o3_ppb", "indice_qualidade_ar", "qualidade_percebida"],
        "Descrição": ["identificador único da medição.", "local onde o sensor está instalado.", "data/hora da medição.", "região da cidade.", "bairro do ponto de monitoramento.", "residencial, industrial, comercial, escolar etc.", "temperatura em °C.", "umidade relativa do ar (%).", "velocidade do vento (km/h).", "precipitação registrada (mm).", "concentração de material particulado fino PM2,5 (µg/m³).", "concentração de material particulado PM10 (µg/m³).", "concentração de monóxido de carbono (ppm).", "concentração de dióxido de nitrogênio (ppb).", "concentração de ozônio (ppb).", "índice calculado a partir dos poluentes.", "percepção da população: Boa, Moderada, Ruim, Péssima etc."]
    })
    
    # Salva o arquivo Original contendo a aba de Dados brutos e o Dicionário
    with pd.ExcelWriter("cidade_alfa_qualidade_ar_original.xlsx", engine='openpyxl') as writer:
        df_original.to_excel(writer, sheet_name='Dados', index=False)
        df_dicionario.to_excel(writer, sheet_name='Dicionario', index=False)
    
    # 2. Processo de ETL (Limpeza de duplicatas para a base ajustada)
    df_ajustado = df_original.drop_duplicates().copy()
    
    # Salva o arquivo Ajustado contendo a aba de Dados limpos e o Dicionário
    with pd.ExcelWriter("cidade_alfa_qualidade_ar_ajustado.xlsx", engine='openpyxl') as writer:
        df_ajustado.to_excel(writer, sheet_name='Dados', index=False)
        df_dicionario.to_excel(writer, sheet_name='Dicionario', index=False)
        
    print("Sucesso! Ambos os arquivos ('original' e 'ajustado') agora contêm as abas 'Dados' e 'Dicionario'.")
