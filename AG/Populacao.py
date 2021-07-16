import math
from itertools import zip_longest
import numpy.random as rd
import numpy as np
from matplotlib import pyplot as plt

try:
    from Trafo.trafo import Trafo
    from Trafo.CONSTANTES import VARIAVEIS, VARIACOES
except:
    from .Trafo import trafo as Trafo

try:
    from .Individuo import Individuo
except:
    from Individuo import Individuo
try:
    from AG.funcoes import calcular_objetivo, verifica_dominancia, e_dominado
except:
    from funcoes import calcular_objetivo, verifica_dominancia, e_dominado


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
    def __init__(self, numero_populacao: int, individuos: list=None, variacoes: dict=None):
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

    def __repr__(self):
        if len(self.individuos) <= 4:
            a_imprimir = self.individuos
        else: a_imprimir = self.individuos[:2] + self.individuos[-2:]
        # import ipdb; ipdb.set_trace()
        a_imprimir = ",\n".join(map(str, a_imprimir))
        a_imprimir = "População: {\n" + f"{a_imprimir}\n" + "}"
        return a_imprimir
    
    @property
    def length(self):
        return len(self.individuos)
    
    def gerar_grafico(self, separado=False, debug=0):
        """
            @param:
                debug: 
                    0: sem nenhuma infomação
                    1: respectivo numero do individuo na população
                    2: Número com a posição do indivíduo no gráfico
                    3: numero da curva de pareto
        """
        fig, ax = plt.subplots()
        plt.title("Gráfico dos objetivos dos individuos na população")
        plt.xlabel("Massa Total [Kg]")
        plt.ylabel("Perda  Total [W]")
        plt.grid(True)
        
        if not separado:
            vetores = {1: self.individuos}
        else: 
            vetores = self.separa_dominantes()
        
        for j, individuos in vetores.items():
            perdas, massas = self.calcular_objetivos(individuos)
            # plt.plot(massas, perdas, leg)
            # input(i)
            if debug:
                for i in range(len(individuos)):
                    titulo = "Trafos"
                    x, y = massas[i], perdas[i]
                    if debug == 2:
                        txt = "{}[{}, {}]".format(i + 1, round(x, 2), round(y, 2))
                    elif debug == 1:
                        txt = str(i + 1)
                    elif debug == 3:
                        txt = str(j)
                        titulo += f" para frente de pareto {j}"
                        
                    ax.annotate(txt, (x, y))
            
            ax.scatter(massas, perdas, label=f"{titulo}")
        
        plt.legend()
        plt.show()
    
    def separa_dominantes(self):
        vetores = {}
        dominados = self.individuos.copy()
        n = 1
        while len(dominados) > 0:
            dominantes,  dominados = self.retira_dominantes(dominados)
            vetores[n] = dominantes
            n += 1
            # print(len(dominantes), len(dominados))
            # input("Aqui")
        
        # import ipdb; ipdb.set_trace()
        return vetores
        
    def retira_dominantes(self, individuos: list):
        # print("inicio: ", len(individuos))
        n_individuos = len(individuos)
        # dominancia = [True] * n_individuos
        dominantes = []
        dominados = []
        
        for i, ind1 in enumerate(individuos):
            domina = True
            for j, ind2 in enumerate(individuos):
                if i == j:
                    continue
                
                if e_dominado(ind1, ind2):
                    # dominancia[i] = False
                    domina = False
                    dominados.append(ind1)
                    break
            # valores = list(filter(e_dominado, zip_longest(individuos, [ind1], fillvalue=ind1)))
            if domina:
                dominantes.append(ind1)
            
            # import ipdb; ipdb.set_trace()
                
        # print(list(enumerate(dominancia, 1)))
        # print(len(dominantes), len(dominados))
        # import ipdb; ipdb.set_trace()
        # self.gerar_grafico()
        return dominantes, dominados
        
    def calcular_objetivos(self, individuos=None):
        if individuos == None:
            individuos = self.individuos
        objetivos = np.array(list(map(calcular_objetivo, individuos)))
        # from ipdb import set_trace; set_trace()
        return np.transpose(objetivos)

    def get_individuo(self, n):
        return self.individuos[n]