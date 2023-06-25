from numpy import interp

tabelas = {
    "2.1": {"oleo": [8, 10, 12], "seco": [4, 6, 8]},
    "2.3": {
        "1": [3],
        "2": [3, 5],
        "3": [5, 7],
        "4": [7, 15],
        "5": [15, 45],
        "6": [45, 80],
        "7": [80, 200],
    },
    "2.4": {
        "Ku": [0.636, 0.786, 0.85, 0.886, 0.907, 0.923, 0.934, 0.942, 0.948],
        "dimensoes_nucleo": [
            [0.707],
            [0.85, 0.526],
            [0.906, 0.707, 0.424],
            [0.934, 0.796, 0.605, 0.358],
            [0.95, 0.846, 0.707, 0.534, 0.313],
            [0.959, 0.875, 0.768, 0.64, 0.483, 0.281],
            [0.967, 0.898, 0.812, 0.707, 0.584, 0.436, 0.255],
            [0.974, 0.914, 0.841, 0.755, 0.654, 0.554, 0.404, 0.234],
            [0.977, 0.929, 0.867, 0.798, 0.707, 0.608, 0.498, 0.37, 0.214],
        ],
    },
    "2.5": {
        "seco": [
            0.37,
            0.46,
            0.49,
            0.525,
            0.5374435665914221,
            0.5469243792325056,
            0.5534424379232505,
            0.5581828442437923,
            0.5617381489841986,
        ],
        "oleo": [
            0.45,
            0.56,
            0.6,
            0.62,
            0.6346952595936796,
            0.6458916478555305,
            0.6535891647855532,
            0.6591873589164786,
            0.6633860045146728,
        ],
    },
    "perda_magnetica": {
        "inducao": [
            0.0,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1.0,
            1.1,
            1.2,
            1.4,
            1.6,
            1.7,
            1.8,
            1.85,
        ],
        "perdas": [
            0.0,
            0.022,
            0.048,
            0.082,
            0.124,
            0.174,
            0.231,
            0.297,
            0.37,
            0.452,
            0.542,
            0.643,
            0.886,
            1.21,
            1.463,
            1.867,
            2.122,
        ],
    },
    "curva_BH": {
        "B": [
            -1.85,
            -1.8,
            -1.7,
            -1.6,
            -1.5,
            -1.4,
            -1.3,
            -1.2,
            -1,
            -0.8,
            -0.6,
            -0.4,
            -0.2,
            0,
            0.2,
            0.4,
            0.6,
            0.8,
            1,
            1.2,
            1.3,
            1.4,
            1.5,
            1.6,
            1.7,
            1.8,
            1.85,
        ],
        "H": [
            -712.275,
            -362.03,
            -118.623,
            -62.081,
            -42.888,
            -34.032,
            -28.97,
            -25.97,
            -22.476,
            -19.53,
            -16.387,
            -12.672,
            -8.03,
            0,
            8.03,
            12.672,
            16.387,
            19.53,
            22.476,
            25.97,
            28.97,
            34.032,
            42.888,
            62.081,
            118.623,
            362.03,
            712.275,
        ],
    },
    "curva_VA": {
        "B": [0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5, 1.6, 1.7, 1.8],
        "S": [
            0,
            0.039,
            0.078,
            0.127,
            0.184,
            0.278,
            0.398,
            0.583,
            0.814,
            1.417,
            1.857,
            2.979,
            7.767,
        ],
    },
}


def teste():
    tabela = tabelas["2.5"]

    Ku = tabelas["2.4"]["Ku"]
    for i in range(len(Ku)):
        try:
            tabela["seco"][i]
        except:
            b, a = Ku[i - 1 : i + 1]
            tabela["seco"].append(a * tabela["seco"][i - 1] / b)
            tabela["oleo"].append(a * tabela["oleo"][i - 1] / b)

    return tabela


# teste()


def tabela_2_1(tipo: str, S: float, tensao: float) -> float:
    dados = tabelas["2.1"][tipo]
    valor = 1 / (30 + tensao)

    if 0 < S <= 10:
        return dados[0] * valor
    if 10 < S <= 250:
        return dados[1] * valor
    if S > 250:
        return dados[2] * valor
    else:
        raise ValueError("Houve um erro ao executar essa função")


def tabela_2_3(area: float) -> int:
    """parâmetros:
    area: float     # em m²
    retorna: int    # numero de degraus entre 1 e 7
    """
    if area >= 200 or area <= 0:
        raise ValueError(f"A a area nao pode ser maior 0.2 m² nem menor 0")

    if area < 3:
        return 1
    tabela = tabelas["2.3"]

    # from ipdb import set_trace; set_trace()

    for key, value in list(tabela.items())[1:]:
        i, j = value
        if i <= area < j:
            return int(key)

    raise ValueError("Houve um erro!!")


def tabela_2_4(numero_degraus: int) -> list:
    numero_degraus -= 1
    tabela = tabelas["2.4"]
    Ku = tabela["Ku"][numero_degraus]
    L = tabela["dimensoes_nucleo"][numero_degraus]

    return Ku, L


def tabela_2_5(tipo: str, numero_degraus: int) -> float:
    numero_degraus -= 1
    tabela = tabelas["2.5"]
    Ku = tabelas["2.4"]["Ku"]
    if numero_degraus > 4:
        numero_degraus = 4
    try:
        return tabela[tipo][numero_degraus]
    except KeyError:
        txt = f'O tipo de transformador "{tipo}" não é suportado.'
        txt += "Os tipos suportados sao: [{}]".format(
            ", ".join([f'"{i}"' for i in tabela.keys()])
        )
        raise KeyError(txt)


def perda_magnetica_do_nucleo(Bm: float) -> float:
    # Essa função vai realizar a interpolação usando método numpy.interp
    # TODO Realizar os testes nas saidas, pois na linha 156 do código MATLAB ocorre um erro.
    # Quando executo a saída é null (not a number)
    b = tabelas["perda_magnetica"]["inducao"]
    p = tabelas["perda_magnetica"]["perdas"]

    P = interp(Bm, b, p)

    return P


def curva_BH(B: float):
    table = tabelas["curva_BH"]

    b = table["B"]
    h = table["H"]

    H = interp(B, b, h)

    return H


def curva_VA(B: float):
    table = tabelas["curva_VA"]

    b = table["B"]
    s = table["S"]

    S = interp(B, b, s)

    return S


if __name__ == "__main__":
    teste()
