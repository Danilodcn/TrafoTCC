
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
        Individuo.trafo.constantes = self.constantes
        Individuo.trafo.calculo_de_dados_do_trafo()
        
        self.populacao = Populacao(
            numero_populacao=self.numero_populacao,
            variacoes=self.variacoes
        )
    
        
    def run_geracao(self):
        #Inicia Selecionando os Indivíduos para o cruzamento
        # import ipdb; ipdb.set_trace()
        
        
        taxa_cruzamento = self.constantes_ag["taxa_cruzamento"]
        n_populacao = len(self.populacao.individuos)
        
        n_individuos_para_crossover = round(taxa_cruzamento * n_populacao)
        # individuos_para_crossover_heuristico = self.populacao.selecao(n_selecionados=taxa_cruzamento)
        crossover_heuristico = self.populacao.crossover_heuristico(
            qtd_heuristico=n_individuos_para_crossover,
            numero_individuos=n_populacao,
        )
        
        crossover_aritmetico = self.populacao.crossover_aritmetico(
            qtd_aritmetico=n_individuos_para_crossover,
            numero_individuos=n_populacao
        )
        
        self.populacao.individuos = self.populacao.selecao(
            self.populacao.individuos + crossover_aritmetico + crossover_heuristico,
            n_selecionados=n_populacao
        )
        # self.populacao.crossover_heuristico(qtd_heuristico, numero_individuos)
