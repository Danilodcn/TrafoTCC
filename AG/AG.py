
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
        
        self.geracao_atual = 0
        
        # import ipdb; ipdb.set_trace()
        self.startUp()
        
    def startUp(self):
        Individuo.trafo.constantes = self.constantes
        Individuo.trafo.calculo_de_dados_do_trafo()
        
    def run(self):
        pass
