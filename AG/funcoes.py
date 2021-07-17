import numpy as np
    
    
def calcular_objetivo(individuo):
    return individuo.calcular_objetivos()

def verifica_dominancia(i1, i2):
    f1 = i1.calcular_objetivos()
    f2 = i2.calcular_objetivos()
    verifica = f1 < f2
    
    if np.all(verifica):
        return 1, [i1]
    
    elif np.any(verifica):
        return 0, (i1, i2)
    
    else:
        return 2, [i2]

    
    # import ipdb; ipdb.set_trace()

def e_dominado(i1, i2 = None):
    try:
        # input(i1)
        i1, i2 = i1
    except TypeError as erro:
        # print(erro)
        pass
    
    # if i1 == i2: 
    #     return False
    
    f1 = i1.calcular_objetivos()
    f2 = i2.calcular_objetivos()
    verifica = f1 <= f2
    
    if np.all(verifica):
        return False
    
    elif np.any(verifica):
        return False
    else:
        return True

def distribui_argumentos(args):
    # import ipdb; ipdb.set_trace()
    funcao, *args = args
    return funcao(*args)

def distribui_argumentos_passando_tupla(args):
    # import ipdb; ipdb.set_trace()
    funcao, *args = args
    # args = args[0]
    return funcao(*args[0])
