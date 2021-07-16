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
