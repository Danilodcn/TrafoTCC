import math
import numpy.random as rd
import numpy as np

try:
    from Trafo.trafo import Trafo
    from Trafo.CONSTANTES import VARIAVEIS, VARIACOES
except:
    from .Trafo import trafo as Trafo

try:
    from .Individuo import Individuo
except:
    from Individuo import Individuo

def create_suproblem(n_obj, n_pop, T):
    """
        @parametros: 
            n_obj = Número de objetos
            n_pop = Número de indivíduos da população
            T = Número de Neighbors 
        @retorno:
            subproblemas: List = Lista de subproblemas
    """



class Populacao(object):
    def __init__(self, numero_populacao: int, individuos: list=None, variacoes=None):
        #import ipdb; ipdb.set_trace()
        try: 
            self.numero_populacao = int(numero_populacao)

            if isinstance(individuos, list) and len(individuos) > 0:
                self.individuos = individuos
            elif isinstance(variacoes, dict) and individuos == None:
                self.variacoes = variacoes
                self.individuos = self.__gera_individuos()
        except Exception as error:
            texto_erro= f'Erro na construção da classe "{Populacao.__name__}". \
                        \nDurante a execução no arquivo "{__name__}" \
                        \nargumentos passados: \n{numero_populacao=}, \
                        \n{individuos=}, \n{variacoes=} \n\nError: {error}, \
                        \n{error.with_traceback}'
            raise AttributeError(texto_erro)

        self.number_of_Neighbors = np.ceil(self.numero_populacao * 0.1)
        self.number_of_Neighbors = min(max(self.number_of_Neighbors, 2), 15)  # TODO porque usei 2 e 15?

    def __gera_individuos(self):
        individuos = [Individuo(variacoes=self.variacoes) for i in range(self.numero_populacao)]
        return individuos
    
    def __len__(self):
        return len(self.individuos)

    @property
    def length(self):
        return len(self.individuos)

    def __repr__(self):
        if len(self.individuos) <= 4:
            a_imprimir = self.individuos
        else: a_imprimir = self.individuos[:2] + self.individuos[-2:]
        # import ipdb; ipdb.set_trace()
        a_imprimir = ",\n".join(map(str, a_imprimir))
        a_imprimir = "População: {\n" + f"{a_imprimir}\n" + "}"
        return a_imprimir
    
    def get_individuo(self, n):
        return self.individuos[n]
    



