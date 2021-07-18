
try:
    from .Populacao import Populacao
    from .Individuo import Individuo
except ImportError:
    from Populacao import Populacao
    from Individuo import Individuo

class AG():
    def __init__(self, **kwargs):
        # import ipdb; ipdb.set_trace()
        self.variacoes = kwargs["variacoes"]
        self.numero_populacao = kwargs["numero_populacao"]
        self.constantes = kwargs["constantes"]
        self.max_geracoes = kwargs["max_geracoes"]
        self.constantes_ag = kwargs["constantes_ag"]
        
        self.geracao_atual = 0
        
        # import ipdb; ipdb.set_trace()
        self.startUp()
        # self.run_geracao()
        
    def startUp(self):
        # Individuo.trafo.constantes = self.constantes
        # Individuo.trafo.calculo_de_dados_do_trafo()
        
        self.populacao = Populacao(
            constantes=self.constantes,
            numero_populacao=self.numero_populacao,
            variacoes=self.variacoes
        )
    
        
    def run_geracao(self, geracao):
        self.geracao_atual = geracao
        #Inicia Selecionando os Indivíduos para o cruzamento
        # import ipdb; ipdb.set_trace()
        
        print("Começou a geração " + str(geracao))
        
        taxa_crossover = self.constantes_ag["taxa_crossover"]
        taxa_mutacao = self.constantes_ag["taxa_mutacao"]
        
        n_frentes = self.constantes_ag["n_frentes"]
        
        # import ipdb; ipdb.set_trace(context=10)
        n_populacao = len(self.populacao.individuos)
        
        n_individuos_para_crossover = round(taxa_crossover * n_populacao)
        # individuos_para_crossover_heuristico = self.populacao.selecao(n_selecionados=taxa_cruzamento)
        
        self.populacao.crossover_heuristico(
            qtd_heuristico=n_individuos_para_crossover,
            numero_individuos=n_populacao,
            n_frentes=n_frentes,
        )
        
        # # import ipdb; ipdb.set_trace(context=10)
        # self.populacao.crossover_aritmetico(
        #     qtd_aritmetico=n_individuos_para_crossover,
        #     numero_individuos=n_populacao,
        #     n_frentes=n_frentes,
        # )
        
        # self.populacao.mutacao(
        #     qtd=n_populacao,
        #     numero_individuos=0,
        #     taxa=taxa_mutacao,
        #     n_frentes=n_frentes,
        # )
        # # import ipdb; ipdb.set_trace(context=10)
        
        # self.populacao.crossover_heuristico(qtd_heuristico, numero_individuos)
        # import ipdb; ipdb.set_trace(context=20)
        
