try: 
    from Trafo.trafo import Trafo
    from Utils.utils import QueryDict 
except:
    from .Trafo.trafo import Trafo
    from .Utils.utils import QueryDict


class Individuo(QueryDict):
    def __init__(variaveis, **kw):
        super().__init__(**kw)

