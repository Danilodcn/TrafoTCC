from typing import List
# from itertools import compress
import numpy.random as rd
import numpy as np


try:
    from Trafo.trafo import Trafo
    from Trafo.CONSTANTES import VARIAVEIS, CONSTANTES_DADAS, VARIACOES
except:
    from .Trafo import trafo as Trafo


class Individuo(object):
    numero_identificao = 0
    trafo = Trafo(CONSTANTES_DADAS)
    def __init__(self, variaveis: dict=None, variacoes: dict=None):
        Individuo.numero_identificao += 1
        self.id = Individuo.numero_identificao
        texto = 'O argumento "variaveis" ou "variacoes" deve ser um dicionário válido'
        texto += f": variaveis >> {variaveis}; variacoes >> {variacoes}"
        self.variacoes = variacoes
        self.max_variacoes = [i[1] for i in self.variacoes.values()]
        self.min_variacoes = [i[0] for i in self.variacoes.values()]
        # import ipdb; ipdb.set_trace()
        
        try:
            e_vazio = variaveis == None
            try:
                e_vazio = np.all(e_vazio)
                # import ipdb; ipdb.set_trace()
            except Exception as e:
                print("Error: ", e)
                import ipdb; ipdb.set_trace()
                
        except:
            e_vazio = False
        
        if e_vazio:
            if not isinstance(variacoes, dict): 
                raise ValueError(texto)
            self.variaveis = self._gera_variaveis_aleatoriamente(variacoes)
            self.nomes = list(variacoes.keys())
        elif isinstance(variaveis, list) or isinstance(variaveis, tuple) or isinstance(variaveis, np.ndarray):
            self.variaveis = np.asarray(variaveis)
            self.nomes = list(variacoes.keys())
        else:
            self.variaveis = np.asarray(list(variaveis.values()))
            self.nomes = list(variaveis.keys())
        
    def __eq__(self, o):
        if not isinstance(o, Individuo):
            return False
        return np.all(self.variaveis == o.variaveis)

    def __len__(self):
        return len(self.variaveis)

    def __repr__(self):
        # lst = [f"{key} = {round(value, 3)}" for key, value in zip(self.nomes, self.variaveis)]
        # a_imprimir = ", ".join(lst)
        # a_imprimir += "(objetivo = {})".format(self.calcular_objetivos())
        a_imprimir = self.id
        return f"Individuo ({a_imprimir})"

    def _gera_variaveis_aleatoriamente(self, variacoes: dict):
        # variaveis = [rd.uniform(i, j) for i, j in variacoes.values()]
        variaveis = rd.uniform(self.min_variacoes, self.max_variacoes)
        # import ipdb; ipdb.set_trace()
        # return dict(zip(variacoes.keys(), variaveis))
        return variaveis

    def calcular_objetivos(self):
        self.objetivos = Individuo.trafo.run(self.variaveis)
        return self.objetivos

    @staticmethod
    def set_constantes_trafo(constantes: dict, constantes_dadas: dict):
        dados = Individuo.trafo.inicia_as_variaveis(constantes_dadas, constantes)
        Individuo.trafo.constantes = dados
        Individuo.trafo.calculo_de_dados_do_trafo()

    def crossover_aritmetico(self, pai):
        alfa = rd.rand(*self.variaveis.shape)
        alfa = alfa / np.linalg.norm(alfa)
        
        filho_1 = alfa * self.variaveis + (1 - alfa) * pai.variaveis
        filho_2 = (1 - alfa) * self.variaveis + alfa * pai.variaveis
        
        # import ipdb; ipdb.set_trace()
        filho_1 = Individuo(variaveis=filho_1, variacoes=self.variacoes,)
        filho_2 = Individuo(variaveis=filho_2, variacoes=self.variacoes,)
        
        return filho_1, filho_2
    
    def crossover_heuristico(self, pai):
        r = rd.rand(*self.variaveis.shape)
        r = r / np.linalg.norm(r)
        
        filho_1 = r * (self.variaveis - pai.variaveis) + self.variaveis
        filho_1 = Individuo(variaveis=filho_1, variacoes=self.variacoes)
        
        # import ipdb; ipdb.set_trace()
        return filho_1

    def mutacao_uniforme(self, taxa: float=1):
        r = rd.rand(*self.variaveis.shape)
        escolha = r < taxa
        variaveis = self._gera_variaveis_aleatoriamente(self.variacoes)
        variaveis_atuais = self.variaveis.copy()
        for i, value in enumerate(variaveis):
            if escolha[i]:
                variaveis_atuais[i] = value
        
        # import ipdb; ipdb.set_trace()
        
        filho = Individuo(variaveis=variaveis_atuais, variacoes=self.variacoes)
    
        return filho
