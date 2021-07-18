import os
from json import load
from unittest import TestCase
from matplotlib import pyplot as plt

try:
    from AG.Populacao import Populacao
    from AG.Individuo import Individuo
    from Trafo.CONSTANTES import VARIACOES, CONSTANTES_DADAS
    from Trafo.trafo import Trafo

except ImportError as error:
    print(f"Erro no import em {__name__}: {error}")
    #import ipdb; ipdb.set_trace()
    from .AG.Individuo import Individuo
    from .Trafo.trafo import Trafo

try:
    from .utils import erro_e_aceitavel, print_dict
except:
    from utils import erro_e_aceitavel, print_dict
    
class Teste_AG_Cria_População(TestCase):
    def setUp(self):
        self.pathjson = "tests/json/AG/"
        self.config = load(open("tests/config.json", "r"))
        self.teste = self.pathjson + f"teste_{self.config['n']}.json"
        self.json = load(open(self.teste))
        variaveis = self.json["variaveis"]
        self.variaveis = dict(zip(VARIACOES.keys(), variaveis))
        self.erro_aceitavel = self.config["error"]
        self.numero_populacao = self.config["npop"]
        self.constantes = self.json["constantes"]
        

    def teste_cria_população(self):
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)
        try:
            None # import ipdb; ipdb.set_trace()
        except Exception as error:
            texto_erro = f"Erro encontrado no Teste. Erro: {error}"
            self.assertTrue(False, msg=texto_erro)


class Teste_AG_População(TestCase):
    def setUp(self):
        self.pathjson = "tests/json/AG/"
        self.config = load(open("tests/config.json", "r"))
        self.teste = self.pathjson + f"teste_{self.config['n']}.json"
        self.json = load(open(self.teste))
        variaveis = self.json["variaveis"]
        self.variaveis = dict(zip(VARIACOES.keys(), variaveis))
        self.erro_aceitavel = self.config["error"]
        self.numero_populacao = self.config["npop"]
        self.constantes = self.json["constantes"]
    
    def teste_calculo_de_todos_os_objetivos_dos_individuos_na_população(self):
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)
        # import ipdb; ipdb.set_trace()
        objetivos = populacao.calcular_objetivos()
        self.assertIsNotNone(objetivos)

    def teste_selecao_dos_individuos_na_população(self):
        if self.config["ag"]:
            return
        
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)
        
        fig, ax = plt.subplots()
        if self.config["grafico"]:
            populacao.gerar_grafico(
                    separado=False, 
                    debug=4, 
                    titulo="ANTES Mutação", 
                    fig=fig, ax=ax, 
                    geracao=1, 
                    color="red"
                )
        
        populacao.individuos = populacao.selecao(
            populacao.individuos, 
            n_selecionados=populacao.numero_populacao / 2, 
            # taxa=.3
        )
        
        if self.config["grafico"]:
            populacao.gerar_grafico(
                separado=False, 
                debug=4, 
                titulo="ANTES e DEPOIS da Seleção", 
                fig=fig, ax=ax, 
                geracao=2, 
                color="yellow"
            )
            plt.show()
        

    def teste_plotagem_de_todos_os_objetivos_dos_individuos_na_população(self):
        if self.config["ag"]:
            return
        
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)
        plotar = self.config["grafico"]
        if plotar:
            populacao.gerar_grafico(separado=True, debug=3, titulo="")
            plt.show()
        else:
            print(f"O teste {self.__class__.__name__} rodou sem executar a plotagem")
    
    def teste_plotagem_das_frentes_de_pareto_nos_individuos_na_população(self):
        if self.config["ag"]:
            return
        
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)
        plotar = self.config["grafico"]
        # plotar = True
        if plotar:
            populacao.gerar_grafico(
                separado=True, 
                debug=3, 
                titulo="Frentes de Pareto Individuais da População"
            )
            
            plt.show()
        else:
            print(f'O teste "Frentes de Pareto Individuais" rodou sem executar a plotagem')
   
    def teste_mutação_dos_individuos(self):
        if self.config["ag"]:
            return
        
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)

        fig, ax = plt.subplots()
        grafico = self.config["grafico"]
        # grafico = True
        if grafico:
            populacao.gerar_grafico(
                separado=False, 
                debug=4, 
                titulo="ANTES Mutação", 
                fig=fig, ax=ax, 
                geracao=1, 
                color="red"
            )
            pass

        populacao.mutacao(qtd=20, taxa=.4, n_frentes=3)
        if grafico:
            populacao.gerar_grafico(
                separado=False, 
                debug=4, 
                titulo="ANTES e DEPOIS Mutação",  
                fig=fig, ax=ax, 
                geracao=2, 
                color="blue"
            )
        
            plt.show()
        else:
            print(f"O teste 'Mutação dos Individuos' rodou sem executar a plotagem")
        
        
    def teste_crossover_heuristico_dos_individuos(self):
        if self.config["ag"]:
            return
        
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)

        fig, ax = plt.subplots()
        grafico = self.config["grafico"]
        # grafico = True
        if grafico:
            populacao.gerar_grafico(
                separado=False, 
                debug=4,
                titulo="ANTES", 
                fig=fig, ax=ax, 
                geracao=1, 
                color="brown"
            )
        qtd = 10
        
        populacao.crossover_heuristico(
            qtd_heuristico=qtd,
            numero_individuos=populacao.numero_populacao,
            n_frentes=3
        )
        
        if grafico:
            populacao.gerar_grafico(
                separado=False, 
                debug=4, 
                titulo="ANTES e DEPOIS do crossover HEURISTICO",  
                fig=fig, ax=ax, 
                geracao=2, 
                color="green"
            )
        
            plt.show()
        else:
            print(f"O teste 'Mutação dos Individuos' rodou sem executar a plotagem")
        
            
    def teste_crossover_aritmetico_dos_individuos(self):
        if self.config["ag"]:
            return
        
        populacao = Populacao(self.constantes, self.numero_populacao, variacoes=VARIACOES)

        fig, ax = plt.subplots()
        grafico = self.config["grafico"]
        # grafico = True
        if grafico:
            populacao.gerar_grafico(
                separado=False, 
                debug=4,
                titulo="ANTES", 
                fig=fig, ax=ax, 
                geracao=1, 
                color="brown"
            )
        qtd = 10
        
        populacao.crossover_aritmetico(
            qtd_aritmetico=qtd,
            numero_individuos=populacao.numero_populacao,
            n_frentes=3
        )
        
        if grafico:
            populacao.gerar_grafico(
                separado=False, 
                debug=4, 
                titulo="ANTES e DEPOIS do crossover ARITMÉTICO",  
                fig=fig, ax=ax, 
                geracao=2, 
                color="green"
            )
            
            plt.show()
            
        else:
            print(f"O teste 'Mutação dos Individuos' rodou sem executar a plotagem")
        
   