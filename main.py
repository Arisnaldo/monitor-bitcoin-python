import tkinter
import os
import winsound
import cotacao  # Nosso arquivo que busca os preços

# CONFIGURAÇÕES E CORES

COR_TEXTO_BRANCO = "#FFFFFF"
COR_VERDE_NEON = "#00FF88"
COR_FUNDO_BOTAO = "#1E1E2E"

# Fontes usadas
FONTE_TITULO = ("Helvetica", 18, "bold")
FONTE_PRECO_GIGANTE = ("Helvetica", 28, "bold")
FONTE_SUBTITULO = ("Helvetica", 12)

# Variável que guarda qual moeda estamos vendo agora (Começa em reais)
moeda_selecionada = "BRL" 

# Configurando onde esta o arquivo de som no computador
DIRETORIO_ATUAL = os.path.dirname(__file__)
CAMINHO_DO_SOM = os.path.join(DIRETORIO_ATUAL, "sons", "aviso.wav")

# FUNÇÕES DO SISTEMA (LÓGICA)

def tocar_som_notificacao():
    """
    Função responsável por tocar o arquivo de audio (.wav)
    sem travar o programa enquanto toca.
    """
    try:
        if os.path.exists(CAMINHO_DO_SOM):
            # SND_ASYNC = Tocar de forma assíncrona (em segundo plano)
            winsound.PlaySound(CAMINHO_DO_SOM, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as erro:
        print(f"Não foi possível tocar o som: {erro}")

def atualizar_dados_na_tela(tocar_som_agora=True):
    """
    Busca o preço atualizado e apresenta na tela.
    Parametro 'tocar_som_agora': se for Verdadeiro, toca o som. se Falso, fica mudo.
    """
    # Busca os dados no arquivo cotacao.py
    preco_bitcoin, preco_dolar = cotacao.buscar_dados(moeda_selecionada)

    if preco_bitcoin:
        # Se encontrou o preço e a ordem é para tocar o som.
        if tocar_som_agora:
            tocar_som_notificacao()

        # Define se o símbolo será R$ ou US$
        simbolo_moeda = "R$" if moeda_selecionada == "BRL" else "US$"
        
        # --- ATUALIZANDO OS TEXTOS NA TELA ---
        # Usamos o 'itemconfig' para modificar um texto que já existe no Canvas
        canvas_fundo.itemconfig(texto_preco_bitcoin, text=f"{simbolo_moeda} {preco_bitcoin:,.2f}")
        
        if moeda_selecionada == "BRL":
            canvas_fundo.itemconfig(texto_preco_dolar, text=f"Dólar Hoje: R$ {preco_dolar:,.2f}")
        else:
            canvas_fundo.itemconfig(texto_preco_dolar, text="Cotação em Dólar (USD)")
            
        canvas_fundo.itemconfig(texto_status, text=f"Atualizado em {moeda_selecionada}")
    else:
        # Caso ocorra erro de conexão
        canvas_fundo.itemconfig(texto_preco_bitcoin, text="Sem Conexão")
        canvas_fundo.itemconfig(texto_status, text="Tentando reconectar...")

    # --- ATUALIZANDO PREÇO ---
    #Atualiza o preço a cada 60.000 milissegundos (1 minuto)
    janela_principal.after(60000, atualizar_dados_na_tela)

def alternar_moeda():
    """
    Função chamada quando clicamos no botão.
    Ela inverte a moeda (Real <-> Dólar).
    """
    global moeda_selecionada
    
    if moeda_selecionada == "BRL":
        moeda_selecionada = "USD"
        botao_trocar_moeda.config(text="Voltar para Reais (BRL)")
    else:
        moeda_selecionada = "BRL"
        botao_trocar_moeda.config(text="Ver em Dólares (USD)")
    
    # Chama a atualização mas avisa: tocar_som_agora = False
    atualizar_dados_na_tela(tocar_som_agora=False)


# INTERFACE GRÁFICA

# Cria a janela principal
janela_principal = tkinter.Tk()
janela_principal.title("Crypto Monitor")

# Define tamanho (Largura x Altura) e não permite redimensionamento
LARGURA_TELA = 400
ALTURA_TELA = 550
janela_principal.geometry(f"{LARGURA_TELA}x{ALTURA_TELA}")
janela_principal.resizable(False, False)

# --- Carregando Imagens ---
try:
    imagem_icone = tkinter.PhotoImage(file="./img/icone.png")
    janela_principal.iconphoto(True, imagem_icone)
except:
    pass # Se não tiver ícone, segue sem.

try:
    imagem_fundo = tkinter.PhotoImage(file="./img/fundo.png")
except:
    imagem_fundo = None
    janela_principal.config(background="#121212")

# --- Criando o Canvas ---
canvas_fundo = tkinter.Canvas(
    janela_principal, 
    width=LARGURA_TELA, 
    height=ALTURA_TELA, 
    highlightthickness=0, 
    background="#121212"
)
canvas_fundo.pack(fill="both", expand=True)

# Imagem de fundo
if imagem_fundo:
    canvas_fundo.create_image(0, 0, image=imagem_fundo, anchor="nw")

# --- Textos Iniciais ---
canvas_fundo.create_text(
    200, 100, 
    text="BITCOIN AGORA", 
    font=FONTE_TITULO, 
    fill=COR_TEXTO_BRANCO
)

# Guardamos este texto em uma variavel para poder mudar o valor dele depois
texto_preco_bitcoin = canvas_fundo.create_text(
    200, 160, 
    text="Carregando...", 
    font=FONTE_PRECO_GIGANTE, 
    fill=COR_VERDE_NEON
)

texto_preco_dolar = canvas_fundo.create_text(
    200, 220, 
    text="---", 
    font=FONTE_SUBTITULO, 
    fill="#AAAAAA"
)

texto_status = canvas_fundo.create_text(
    200, 520, 
    text="Iniciando...", 
    font=("Arial", 8), 
    fill="#666666"
)

# --- Botão ---
botao_trocar_moeda = tkinter.Button(
    janela_principal, 
    text="Ver em Dólares (USD)", 
    command=alternar_moeda,
    background=COR_FUNDO_BOTAO, 
    foreground="white", 
    font=("Arial", 10, "bold"), 
    borderwidth=0, 
    padx=20, 
    pady=10, 
    activebackground=COR_VERDE_NEON
)

# Posiciona o botão
botao_trocar_moeda.place(x=100, y=430, width=200)

# --- Iniciando o Ciclo ---
# Espera 1 segundo (1000ms) e roda a primeira atualização
janela_principal.after(1000, atualizar_dados_na_tela) 

# Mantém a janela aberta
janela_principal.mainloop()