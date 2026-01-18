import requests

def buscar_preco_coinbase(moeda):
    try:
        #Api COINBASE
        url = f"https://api.coinbase.com/v2/prices/BTC-{moeda}/spot"
        
        resposta = requests.get(url)
        dados = resposta.json()
        
        #Float serve para transformar o texto em número
        preco = float(dados["data"]["amount"])
        
        print(f"Bitcoin em {moeda}: {preco:,.2f}")
        return preco
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None

# Testando com duas moedas
buscar_preco_coinbase("USD")
buscar_preco_coinbase("BRL")