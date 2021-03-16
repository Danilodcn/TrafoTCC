VARIAVEIS = {
    "Jbt": 1,   # Densidade de corrente na baixa tensao [A/mm²]
    "Jat": 1,   # Densidade de corrente na alta tensao [A/mm²]
    "Bm": 1,    # Densidade de fluxo máximo na coluna do núcleo [T]
    "Ksw": 1,   # Fator de espaço no núcleo do Transformador (formula 3.9)
    "kt": 1,    # Relação volt/espira
    "Rjan": 1,  # Relação entre largura e altura da janela do Transformador
    "rel": 1,   # representa a relação entre a área do núcleo e a área da culatra
}

CONSTANTES_DADAS = {
    "conexao": (1,1),    #tipo de conexão usada no Trafo ex: (delta, estrela)
    "Ke": 1,        # Constante de empilhamento fornecido pelo fabricante das chapas do núcleo
    "S": 1,         # Potencia do Transformador [VA]
    "Nfases": 1,    # Numero de fases do Transformador
    "f": 60,        # Frequencia da rede em Hz
    "V1": 1,        # Tensao no primário [Kv]
    "V2": 1,        # Tensao no secundário [Kv]
    "tipo": "str",  # Tipo de refrigeração do transformador
    "Dfe": 1,       # Densidade do ferroem [Kg/m³]
}

TABELAS = {}


if __name__ == "__main__":
    print(", ".join(VARIAVEIS.keys()))
