try:
    from AG.Individuo import Individuo
    from Trafo.trafo import Trafo

except:
    from .AG.Individuo import Individuo
    from .Trafo.trafo import Trafo


from json import load
import os

from unittest import TestCase


class Teste_AG(TestCase):

    def setUp(self):
        self.pathjson = "tests/json/AG"
        self.config = load(open("tests/config.json", "r"))
    
    def test_cria_inidividuo(self):
        
        ...