try:
    from AG.Individuo import Individuo
    from Trafo.trafo import Trafo

except ImportError as error:
    print(f"Erro no import em {__name__}: {error}")
    from .AG.Individuo import Individuo
    from .Trafo.trafo import Trafo


from json import load
import os

from unittest import TestCase


class TesteAG_Criacao_Individuo(TestCase):

    def setUp(self):
        self.pathjson = "tests/json/AG/"
        self.config = load(open("tests/config.json", "r"))
        self.teste = self.pathjson + f"teste_{self.config['n']}.json"
    

    def test_cria_inidividuo(self):
        json_ = load(open(self.teste))
        
        variaveis = json_["variaveis"]
        _ind = Individuo(variaveis)
        # import ipdb; ipdb.set_trace()

class TesteAG_Individuo(TestCase):
    def setUp(self):
        ...