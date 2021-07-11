try:
    from AG.Individuo import Individuo
    from Trafo.CONSTANTES import VARIACOES
    from Trafo.trafo import Trafo

except ImportError as error:
    print(f"Erro no import em {__name__}: {error}")
    #import ipdb; ipdb.set_trace()
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
    

    def test_cria_individuo(self):
        json_ = load(open(self.teste))
        
        variaveis = json_["variaveis"]
        try:
            ind = Individuo(variacoes=VARIACOES)
            #import ipdb; ipdb.set_trace()
        except Exception as e:
            msg = f"{__name__} >> Erro na criação do indivíduo: {e}"
            self.assertTrue(False, msg)


class TesteAG_Individuo(TestCase):
    def setUp(self):
        self.variacoes = VARIACOES

    def test_qualquer(self):
        self.assertTrue(True)