import numpy.random as rd

try:
    from Trafo.trafo import Trafo
    from Trafo.CONSTANTES import VARIAVEIS, VARIACOES
except:
    from .Trafo import trafo as Trafo

try:
    from .Individuo import Individuo
except:
    from Individuo import Individuo


class Populacao(object):
    def __init__(self, numero_populacao: int, individuos: list=None,variacoes=VARIACOES):
        self.variacoes = variacoes
        self.numero_populacao = numero_populacao
        self.individuos = individuos if individuos == None else self.__gera_individuos()

    def __gera_individuos(self):
        individuos = [Individuo(self.variacoes) for i in range(self.numero_populacao)]
    
    def __len__(self):
        return len(self.individuos)
    
    def get_individuo(self, n):
        return self.individuos[n]
    



