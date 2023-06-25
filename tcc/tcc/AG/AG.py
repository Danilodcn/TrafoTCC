import itertools as it

import pandas as pd

from tcc.AG.Individuo import Individuo
from tcc.AG.Populacao import Populacao
from tcc.trafo.CONSTANTES import VARIAVEIS


class AG:
    def __init__(self, **kwargs):
        self.variacoes = kwargs["variacoes"]
        self.numero_populacao = kwargs["numero_populacao"]
        self.constantes = kwargs["constantes"]
        self.max_geracoes = kwargs["max_geracoes"]
        self.constantes_ag = kwargs["constantes_ag"]

        self.geracao_atual = 0

        self.startUp()
        # self.run_geracao()

    def startUp(self):
        # Individuo.trafo.constantes = self.constantes
        # Individuo.trafo.calculo_de_dados_do_trafo()

        self.populacao = Populacao(
            constantes=self.constantes,
            numero_populacao=self.numero_populacao,
            variacoes=self.variacoes,
        )

    def run_geracao(self, geracao):
        self.geracao_atual = geracao
        # Inicia Selecionando os Indivíduos para o cruzamento

        taxa_crossover = self.constantes_ag["taxa_crossover"]
        taxa_mutacao = self.constantes_ag["taxa_mutacao"]
        n_frentes = self.constantes_ag["n_frentes"]

        n_populacao = len(self.populacao.individuos)
        n_individuos_para_crossover = round(taxa_crossover * n_populacao)
        # individuos_para_crossover_heuristico = self.populacao.selecao(n_selecionados=taxa_cruzamento)
        self.populacao.crossover_heuristico(
            qtd_heuristico=n_individuos_para_crossover,
            numero_individuos=n_populacao,
            n_frentes=n_frentes,
        )

        self.populacao.crossover_aritmetico(
            qtd_aritmetico=n_individuos_para_crossover,
            numero_individuos=n_populacao,
            n_frentes=n_frentes,
        )

        # self.populacao.mutacao(
        #     qtd=n_populacao,
        #     numero_individuos=0,
        #     taxa=taxa_mutacao,
        #     n_frentes=n_frentes,
        # )

        # self.populacao.crossover_heuristico(qtd_heuristico, numero_individuos)

    def gerar_populacao_inicial(self, n):
        individuos = it.chain(
            *(self.populacao.gera_individuos() for i in range(n))
        )
        self.populacao.individuos.update(individuos)
        self.populacao.individuos = self.populacao.selecao(
            n_selecionados=self.numero_populacao,
            n_frentes=8,
        )

    def run(self):
        # file = "individuos.xlsx"
        names = ["Id"] + list(VARIAVEIS.keys()) + ["PerdasT", "Mativa"]
        self.df = pd.DataFrame(columns=names)

        # self.df = pd.read_excel(file)

        self.gerar_populacao_inicial(3)

        # ind = self.populacao.individuos.copy()

        # for i in ind:
        #     var = [int(i.id)] + list(i.variaveis)
        #     self.df.loc[-1] = var
        #     self.df.index += 1
        #     self.df.sort_index()

        for geracao in range(1, self.max_geracoes + 1):
            print("geração: ", geracao)

            self.run_geracao(geracao)
            ind = self.populacao.individuos.copy()

            for i in ind:
                obj = i.calcular_objetivos(penalidade=False)

                var = [int(i.id)] + list(i.variaveis) + list(obj)
                self.df.loc[-1] = var
                self.df.index += 1
                self.df.sort_index()

            yield geracao
