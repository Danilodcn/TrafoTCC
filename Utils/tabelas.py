tabelas = {
    "2.3": {
        "1": [3], 
        "2": [3, 5], 
        "3": [5, 7], 
        "4": [7, 15], 
        "5": [15, 45], 
        "6": [45, 80], 
        "7": [80, 200]
    }, 
    "2.4": {
        "Ku": [0.636, 0.786, 0.85, 0.886, 0.907, 0.923, 0.934, 0.942, 0.948], 
        "dimensoes_nucleo":[
            [0.707], 
            [0.85, 0.526], 
            [0.906, 0.707, 0.424], 
            [0.934, 0.796, 0.605, 0.358], 
            [0.95, 0.846, 0.707, 0.534, 0.313], 
            [0.959, 0.875, 0.768, 0.64, 0.483, 0.281], 
            [0.967, 0.898, 0.812, 0.707, 0.584, 0.436, 0.255], 
            [0.974, 0.914, 0.841, 0.755, 0.654, 0.554, 0.404, 0.234], 
            [0.977, 0.929, 0.867, 0.798, 0.707, 0.608, 0.498, 0.37, 0.214]
            ]
        }, 
    "2.5":{
        "seco": [0.37, 0.46, 0.49, 0.525, 0.505], 
        "oleo": [0.45, 0.56, 0.6, 0.62, 0.625]
    }
}


def tabela_2_3(area: float) -> int:
    """paramentros:
        area: float     # em m²
        retorna: int    # numero de degraus entre 1 e 7 
    """
    if area >= 200 or area <= 0:
        raise ValueError(f"A a area nao pode ser maior 0.2 m² nem menor 0")
    
    if area < 3: return 1
    tabela = tabelas["2.3"]

    # from ipdb import set_trace; set_trace()

    for key, value in list(tabela.items())[1:]:
        i, j = value
        if i <= area < j: return int(key)


    raise ValueError("Houve um erro!!")

def tabela_2_4(numero_degraus: int) -> list:
    tabela = tabelas["2.4"]
    Ku = tabela["Ku"][numero_degraus]
    L = tabela["dimensoes_nucleo"][numero_degraus]

    return Ku, L

def tabela_2_5(tipo: str, numero_degraus: int) -> float:
    tabela = tabelas["2.5"]
    if numero_degraus > 5:
        numero_degraus = 5
    try:
        return tabela[tipo][numero_degraus]
    except KeyError:
        txt = f'O tipo de transformador "{tipo}" não é suportado.'
        txt += 'Os tipos suportados sao: [{}]'.format(', '.join([f'"{i}"' for i in tabela.keys()]))
        raise KeyError(txt)