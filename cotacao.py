import requests

def buscar_dados(moeda_destino="BRL"):
    try:
        #Busca bitcoin na coinbase
        url_btc = f"https://api.coinbase.com/v2/prices/BTC-{moeda_destino}/spot"
        resp_btc = requests.get(url_btc).json()
        preco_btc = float(resp_btc["data"]["amount"])

        #Busca a cotação do Dólar (Se a moeda destino for BRL)
        preco_dolar = 1.0
        if moeda_destino == "BRL":
            url_dolar = "https://economia.awesomeapi.com.br/last/USD-BRL"
            resp_dolar = requests.get(url_dolar).json()
            preco_dolar = float(resp_dolar["USDBRL"]["bid"])

        return preco_btc, preco_dolar
    
    except Exception as e:
        print(f"Erro: {e}")
        return None, None