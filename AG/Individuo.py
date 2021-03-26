try: 
    from Trafo.trafo import Trafo
    from Trafo.CONSTANTES import VARIAVEIS
    from Utils.utils import QueryDict 
except:
    from .Trafo.trafo import Trafo
    from .Trafo.CONSTANTES import VARIAVEIS
    from .Utils.utils import QueryDict


class Individuo(QueryDict):
    def __init__(self, variaveis):
        kw = dict(zip(VARIAVEIS.keys(), variaveis))
        super().__init__(**kw)
    
    def calcula_perdas(self, trafo: Trafo):
        self.perdas = trafo.calculo_das_perdas_do_trafo(self)


    
        


