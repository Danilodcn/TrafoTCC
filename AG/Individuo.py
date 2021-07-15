from typing import List

import numpy.random as rd


try:

    from Trafo.trafo import Trafo

    from Trafo.CONSTANTES import VARIAVEIS, CONSTANTES_DADAS, VARIACOES

except:

    from .Trafo import trafo as Trafo



class Individuo:

    trafo = Trafo(CONSTANTES_DADAS)

    def __init__(self, variaveis: dict=None, variacoes: dict=None):

        texto = 'O argumento "variaveis" ou "variacoes" deve ser um dicionário válido'

        texto += f": variaveis >> {variaveis}; variacoes >> {variacoes}"

        if variaveis == None:
            if not isinstance(variacoes, dict): 

                raise ValueError(texto)

            self.variaveis = self._gera_variaveis_aleatoriamente(variacoes)
        elif not isinstance(variaveis, dict):

            raise ValueError(texto)
        else:

            self.variaveis = variaveis


    def __eq__(self, o):

        return self.variaveis == o.variaveis

    def __len__(self):
        return len(self.variaveis)


    def __repr__(self):

        lst = [f"{key} = {round(value, 3)}" for key, value in self.variaveis.items()]

        a_imprimir = ", ".join(lst)

        return f"Individuo ({a_imprimir})"


    def _gera_variaveis_aleatoriamente(self, variacoes: dict):

        variaveis = [rd.uniform(i, j) for i, j in variacoes.values()]

        return dict(zip(variacoes.keys(), variaveis))


    def calcula_objetivo(self):

        self.objetivos = Individuo.trafo.run(self.variaveis)

        return self.objetivos


    @staticmethod
    def set_constantes_trafo(constantes: dict):

        dados = Individuo.trafo.inicia_as_variaveis(CONSTANTES_DADAS, constantes)

        Individuo.trafo.constantes = dados

        Individuo.trafo.calculo_de_dados_do_trafo()

    def crossover_aritmetico(self, individuo, *args: List):

        args.append(individuo)
        
    

"""

VARIACOES = {

            "Jbt": (1.2, 1.4),

            "Jat": (1.4, 1.6),

            "Bm": (1.5, 1.6),

            "Kws": (6, 7),

            "kt": (0.45, 0.55),

            "Rjan": (3.4, 3.6),

            "rel": (1.1, 1.2),

            }

# i = Individuo(variacoes=VARIACOES)

# import ipdb; ipdb.set_trace()"""



#import ipdb; ipdb.set_trace()

