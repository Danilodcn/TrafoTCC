import math, random
import itertools as it
from collections.abc import Iterator, Iterable
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
    from AG.funcoes import (
            calcular_objetivo, 
            verifica_dominancia, 
            e_dominado, 
            distribui_argumentos, 
            distribui_argumentos_passando_tupla
        ) 
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
    def __init__(self, 
        constantes: dict, numero_populacao: int, 
        individuos: list=None, variacoes: dict=None
    ):
        #import ipdb; ipdb.set_trace()
        Individuo.trafo.constantes = constantes
        Individuo.trafo.calculo_de_dados_do_trafo()
        
        try: 
            self.numero_populacao = int(numero_populacao)
            if isinstance(individuos, list) and len(individuos) > 0:
                self.individuos = individuos
            elif isinstance(variacoes, dict) and individuos == None:
                self.variacoes = variacoes
                self.individuos = self.gera_individuos()
        except Exception as error:
            texto_erro= f'Erro na construção da classe "{Populacao.__name__}". \
                        \nDurante a execução no arquivo "{__name__}" \
                        \nargumentos passados: \n{numero_populacao=}, \
                        \n{individuos=}, \n{variacoes=} \n\nError: {error}, \
                        \n{error.with_traceback}'
            raise AttributeError(texto_erro)

        self.number_of_Neighbors = np.ceil(self.numero_populacao * 0.1)
        self.number_of_Neighbors = min(max(self.number_of_Neighbors, 2), 15)  # TODO porque usei 2 e 15?
        
    def gera_individuos(self):
        return {Individuo(variacoes=self.variacoes) for i in range(self.numero_populacao)}
    
    def __len__(self):
        return len(self.individuos)

    def __repr__(self):
        if len(self.individuos) <= 4:
            a_imprimir = self.individuos
        else: a_imprimir = self.individuos[:2] + ["..."] + self.individuos[-2:]
        # import ipdb; ipdb.set_trace()
        a_imprimir = ",\n\t".join(map(str, a_imprimir))
        a_imprimir = "População: {\n" + f"\t{a_imprimir}\n" + "}" + " com {} individuos".format(len(self.individuos))
        return a_imprimir
    
    @property
    def length(self):
        return len(self.individuos)
    
    def gerar_grafico(self, separado=False, debug=0, titulo="", fig=None, ax=None, geracao=1, color=None):
        """
            @param:
                debug: 
                    0: sem nenhuma infomação
                    1: respectivo numero do individuo na população
                    2: Número com a posição do indivíduo no gráfico
                    3: numero da curva de pareto
                    4: TODO
        """
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        plt.title(titulo)
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
                    label = "Trafos"
                    x, y = massas[i], perdas[i]
                    y *= random.triangular(0.999, 1.001)
                    x *= random.triangular(0.999, 1.001)
                    
                    if debug == 1:
                        txt = str(i + 1)
                    elif debug == 2:
                        txt = "{}[{}, {}]".format(i + 1, round(x, 2), round(y, 2))
                    elif debug == 3:
                        txt = str(j)
                        label += f"{j} {titulo}"
                    elif debug == 4:
                        txt = str(geracao)
                        label = f"Geração {geracao}"
                        
                    ax.annotate(txt, (x, y))
            
            ax.scatter(massas, perdas, label=f"{label} com {len(perdas)}", color=color)
        
        plt.legend()
        # print(len(self.individuos))
        plt.show()
        # import ipdb; ipdb.set_trace()
        
    def separa_dominantes(self, individuos: list=None):
        vetores = {}
        
        if individuos == None:
            individuos = self.individuos.copy()
                    
        # input(len(dominados))
        n = 1
        while len(individuos) > 0:
            dominantes,  individuos = self.retira_dominantes(individuos)
            vetores[n] = dominantes
            n += 1
            # print(len(dominantes), len(dominados))
            # input("Aqui")
        
        # import ipdb; ipdb.set_trace()
        return vetores
        
    def retira_dominantes(self, individuos: Iterator):
        # print("inicio: ", len(individuos))
        # import ipdb; ipdb.set_trace()
        individuos = list(individuos)
        # n_individuos = len(individuos)
        # dominancia = [True] * n_individuos
        dominantes = []
        dominados = []
        
        for i, ind1 in enumerate(individuos):
            domina = True
            for j, ind2 in enumerate(individuos):
                if i == j:
                    continue                        
                try:
                    # numero, ind = verifica_dominancia(ind1, ind2)
                    # if numero == 1 or numero == 2:
                    #     domina = False
                    #     dominados.append(ind1)
                    #     break  
                    if e_dominado(ind1, ind2):
                        # dominancia[i] = False
                        domina = False
                        dominados.append(ind1)
                        break
                except:
                    import ipdb; ipdb.set_trace(context=10)
            if domina:
                dominantes.append(ind1)
            
            # import ipdb; ipdb.set_trace()
        
        return dominantes, dominados
        
    def calcular_objetivos(self, individuos=None):
        if individuos == None:
            individuos = self.individuos
        objetivos = np.array(list(map(calcular_objetivo, individuos)))
        # from ipdb import set_trace; set_trace()
        return np.transpose(objetivos)

    def get_individuo(self, n):
        return self.individuos[n]

    def mutacao(self, qtd, numero_individuos, taxa, n_frentes):
        para_mutacao = self.selecao(n_selecionados=qtd, n_frentes=n_frentes)
        # para_mutacao = self.selecao(n_selecionados=qtd)
        
        taxa = [taxa] * len(para_mutacao)
        
        depois_mutacao = map(
            distribui_argumentos, 
            it.zip_longest([], para_mutacao, taxa, fillvalue=Individuo.mutacao_uniforme)
        )
        
        # from ipdb import set_trace; set_trace()
        self.individuos.update(depois_mutacao)
        if numero_individuos:
            self.individuos = self.selecao(
                n_selecionados=numero_individuos,
                n_frentes=n_frentes,
        )
    
    
    def selecao(self, individuos: list=None, n_selecionados: int=0, n_frentes=3):
        if individuos == None:
            individuos = self.individuos.copy()
            
        # import ipdb; ipdb.set_trace()
        n_selecionados = math.ceil(n_selecionados)
        # taxa_escolha = rd.rand(3)
        selecionados = set()
        n = 0
        iteracao = 0
        while n < n_selecionados:
            iteracao += 1
            dominantes, individuos = self.retira_dominantes(individuos)
            
            # import ipdb; ipdb.set_trace(context=10)
            if  iteracao > n_frentes or len(individuos) == 0:
                n_a_selecionar = n_selecionados - len(selecionados)
                selecionados.update(rd.choice(individuos + dominantes, n_a_selecionar, False))
                break
                
            n_dominantes = len(dominantes)

            if n_dominantes + n > n_selecionados:
                n_a_selecionar = n_selecionados - n
                selecionados.update(rd.choice(dominantes, n_a_selecionar, False))
                n = len(selecionados)
                
            else:
                n_a_selecionar = n_dominantes
                selecionados.update(dominantes)
                n = len(selecionados)
                continue
            
        try:
            assert len(selecionados) == n_selecionados
        except:
            import ipdb; ipdb.set_trace(context=10)
            
        return selecionados    
        
    def _crossover(self, qtd_heuristico, qtd_aritmetico, numero_individuos):
        #Crossover Heuristico
        para_heuristico = rd.choice(self.individuos, qtd_heuristico)
        iter_para_heuristico = it.permutations(para_heuristico, 2)
        
        depois_crossover_heuristico = list(
            map(
                distribui_argumentos_passando_tupla,
                it.zip_longest([], iter_para_heuristico, fillvalue=Individuo.crossover_heuristico)
            )
        )
        
        # import ipdb; ipdb.set_trace()       
        #Crossover Aritmético
        para_aritmetico = rd.choice(self.individuos, qtd_aritmetico)
        iter_para_aritmetico = it.permutations(para_aritmetico, 2)
        
        depois_crossover_aritmetico = list(
            map(
                distribui_argumentos_passando_tupla,
                it.zip_longest([], iter_para_aritmetico, fillvalue=Individuo.crossover_aritmetico)
            )
        )
        
        # import ipdb; ipdb.set_trace()
        depois_crossover_aritmetico += self.individuos
                
        return self.selecao(
            individuos=depois_crossover_aritmetico + depois_crossover_heuristico, 
            n_selecionados=numero_individuos,
        )
        # self.individuos = [ind for ind in self.individuos if not ind in dominantes]
        
        # self.individuos += dominantes
        
    def crossover_heuristico(self, qtd_heuristico, numero_individuos, n_frentes):
        #Crossover Heuristico
        # para_heuristico = rd.choice(self.individuos, qtd_heuristico)
        para_heuristico = self.selecao(n_selecionados=qtd_heuristico, n_frentes=n_frentes)
        # import ipdb; ipdb.set_trace(context=10)
        
        iter_para_heuristico = it.permutations(para_heuristico, 2)
        
        depois_crossover_heuristico = map(
            distribui_argumentos_passando_tupla,
            it.zip_longest([], iter_para_heuristico, fillvalue=Individuo.crossover_heuristico)
        )
        
        # import ipdb; ipdb.set_trace(context=10)
        self.individuos.update(depois_crossover_heuristico)
        
        self.individuos = self.selecao(
            n_selecionados=numero_individuos,
            n_frentes=n_frentes
        )

    def crossover_aritmetico(self, qtd_aritmetico, numero_individuos, n_frentes):
        # import ipdb; ipdb.set_trace()       
        #Crossover Aritmético
        # para_aritmetico = rd.choice(self.individuos, qtd_aritmetico)
        para_aritmetico = self.selecao(n_selecionados=qtd_aritmetico, n_frentes=n_frentes)
        iter_para_aritmetico = it.permutations(para_aritmetico, 2)
        
        depois_crossover_aritmetico = map(
            distribui_argumentos_passando_tupla,
            it.zip_longest([], iter_para_aritmetico, fillvalue=Individuo.crossover_aritmetico)
        )
        
        self.individuos.update(depois_crossover_aritmetico)
        
        # import ipdb; ipdb.set_trace(context=20)
        
        self.individuos = self.selecao(
            n_selecionados=numero_individuos,
            n_frentes=n_frentes,
        )
        