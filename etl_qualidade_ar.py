import pandas as pd
import requests
from datetime import datetime

def executar_etl():
    print("Buscando dados reais de qualidade do ar via API...")
    
    # Token público de demonstração da API WAQI para Grande São Paulo / Região
    token = "demo"
    cidade = "sao paulo"
    url = f"https://api.waqi.info/feed/{cidade}/?token={token}"
    
    try:
        response = requests.get(url, timeout=10)
        dados = response.json()
        
        if dados.get("status") == "ok":
            h = dados["data"]
            iaqi = h.get("iaqi", {})
            
            # Mapeando os dados reais para a estrutura exata exigida pelas colunas
            registro_real = {
                'id_coleta': [f"COL_{datetime.now().strftime('%Y%m%d%H%M')}"],
                'id_ponto_monitoramento': [f"PNT_{h.get('idx', '001')}"],
                'data_coleta': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'regiao': ["Metropolitana"],
                'bairro': [h.get('city', {}).get('name', 'Sao Paulo')],
                'tipo_area': ["Urbana"],
                'temperatura_c': [iaqi.get('t', {}).get('v', 25.0)],
                'umidade_%': [iaqi.get('h', {}).get('v', 50)],
                'velocidade_vento_kmh': [iaqi.get('w', {}).get('v', 10.0)],
                'chuva_mm': [0.0],
                'pm25_ug_m3': [iaqi.get('pm25', {}).get('v', 20.0)],
                'pm10_ug_m3': [iaqi.get('pm10', {}).get('v', 40.0)],
                'co_ppm': [iaqi.get('co', {}).get('v', 0.5)],
                'no2_ppb': [iaqi.get('no2', {}).get('v', 20.0)],
                'o3_ppb': [iaqi.get('o3', {}).get('v', 35.0)],
                'indice_qualidade_ar': [h.get('aqi', 45)],
                'qualidade_percebida': ["Boa" if h.get('aqi', 45) <= 50 else "Moderada"]
            }
            
            df = pd.DataFrame(registro_real)
            
            nome_arquivo = "cidade_alfa_qualidade_ar_ajustado.xlsx"
            df.to_excel(nome_arquivo, index=False)
            print(f"Sucesso! Dados reais da API salvos na planilha: {nome_arquivo}")
        else:
            print("Erro ao retornar dados da API.")
            
    except Exception as e:
        print(f"Falha na conexão com a API: {e}")

if __name__ == "__main__":
    executar_etl()
