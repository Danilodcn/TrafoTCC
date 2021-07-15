import numpy as np

def print_dict(dicionario: dict[float, float], simbolo: str = "-") -> str:
    lista = []
    for key, value in dicionario.items():
        txt = str(key) + " = " + f"{simbolo} ".join(map(str, value))
        lista.append(txt)
    
    return ", ".join(lista)

def erro_e_aceitavel(a: float, b: float, error: float) -> bool:
    if a == 0:
        if b == 0: return True
        else: return False
    return abs((a - b) / a) <= error 

def convert_dict_to_numpy(_dict: dict, format=np.float32):
    names = list(_dict.keys())
    formats = [format] * len(names)
    dtype = dict(names=names, formats=formats)
    return np.array(list(_dict.values()), dtype=dtype)

x = convert_dict_to_numpy({
    "Casa": 2,
    "Vida": 5,
})

print(repr(x))