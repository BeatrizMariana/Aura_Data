import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def executar_etl():
    print("Gerando dataset ampliado com 5.000 linhas...")
    
    # 10 estações distribuídas pelas regiões da cidade
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
    
    # 10 estações x 500 registros horários cada = 5.000 linhas no total
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
            
            if aqi <= 50:
                qualidade = "Boa"
            elif aqi <= 100:
                qualidade = "Moderada"
            elif aqi <= 199:
                qualidade = "Ruim"
            else:
                qualidade = "Muito Ruim"
            
            registro = {
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
            }
            registros.append(registro)
            contador += 1

    df = pd.DataFrame(registros)
    nome_arquivo = "cidade_alfa_qualidade_ar_ajustado.xlsx"
    df.to_excel(nome_arquivo, index=False)
    print(f"Sucesso! Planilha gerada com {len(df)} linhas e todas as colunas exigidas.")

if __name__ == "__main__":
    executar_etl()
